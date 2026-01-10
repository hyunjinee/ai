"""
코딩 에이전트 핵심 로직
LangGraph를 사용한 ReAct 스타일 에이전트
"""

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from h.tools import ALL_TOOLS

# Ollama 모델 프리픽스
OLLAMA_PREFIX = "ollama:"

# 추천 Ollama 모델들
OLLAMA_MODELS = [
    "qwen2.5-coder:14b",
    "qwen2.5-coder:7b",
    "codellama:13b",
    "deepseek-coder:6.7b",
    "llama3.1:8b",
]

SYSTEM_PROMPT = """당신은 전문 소프트웨어 개발자 AI 에이전트입니다. 
사용자의 요청에 따라 코드를 작성, 수정, 분석하고 터미널 명령을 실행할 수 있습니다.

## 사용 가능한 도구들

1. **read_file**: 파일 내용 읽기
2. **write_file**: 새 파일 작성 또는 전체 덮어쓰기
3. **edit_file**: 파일의 특정 부분 수정 (old_string → new_string)
4. **list_directory**: 디렉토리 내용 조회
5. **run_command**: 터미널 명령 실행
6. **search_files**: 파일 이름으로 검색
7. **grep_search**: 파일 내용에서 텍스트 검색

## 작업 원칙

1. **먼저 이해하기**: 코드를 수정하기 전에 항상 먼저 파일을 읽어서 내용을 파악
2. **점진적 변경**: 큰 변경은 여러 단계로 나누어 진행
3. **검증하기**: 변경 후 필요하면 테스트나 린트 실행
4. **명확한 설명**: 무엇을 했고 왜 했는지 설명

## 코드 작성 스타일

- 깔끔하고 읽기 쉬운 코드 작성
- 적절한 주석 추가
- 타입 힌트 사용 (Python의 경우)
- 에러 핸들링 고려

현재 작업 디렉토리를 확인하려면 list_directory를 사용하세요.
"""


class AgentState(TypedDict):
    """에이전트 상태"""

    messages: Annotated[list, add_messages]


def create_llm(model_name: str, temperature: float = 0.0):
    """모델 이름에 따라 적절한 LLM 인스턴스 생성

    Args:
        model_name: 모델 이름 (ollama:모델명 또는 OpenAI 모델명)
        temperature: 생성 온도

    Returns:
        LLM 인스턴스
    """
    if model_name.startswith(OLLAMA_PREFIX):
        # Ollama 모델
        ollama_model = model_name[len(OLLAMA_PREFIX):]
        return ChatOllama(model=ollama_model, temperature=temperature)
    else:
        # OpenAI 모델
        return ChatOpenAI(model=model_name, temperature=temperature)


def create_agent(model_name: str = "gpt-4o", temperature: float = 0.0):
    """코딩 에이전트 생성

    Args:
        model_name: 모델 이름 (ollama:모델명 또는 OpenAI 모델명)
        temperature: 생성 온도 (0.0 = 결정적, 1.0 = 창의적)

    Returns:
        컴파일된 LangGraph 에이전트
    """
    # LLM 설정
    llm = create_llm(model_name, temperature)
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    # 도구 노드
    tool_node = ToolNode(ALL_TOOLS)

    def agent_node(state: AgentState) -> dict:
        """에이전트 노드 - LLM 호출"""
        messages = state["messages"]

        # 시스템 메시지가 없으면 추가
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def should_continue(state: AgentState) -> str:
        """다음 단계 결정 - 도구 호출 여부 확인"""
        messages = state["messages"]
        last_message = messages[-1]

        # AI 메시지이고 도구 호출이 있으면 도구 실행
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"

        # 그 외에는 종료
        return END

    # 그래프 구성
    graph = StateGraph(AgentState)

    # 노드 추가
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # 엣지 추가
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


class CodingAgent:
    """코딩 에이전트 래퍼 클래스"""

    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.0):
        self.graph = create_agent(model_name, temperature)
        self.messages: list = []

    def chat(self, user_input: str) -> str:
        """사용자 입력을 처리하고 응답 반환

        Args:
            user_input: 사용자 메시지

        Returns:
            에이전트 응답 텍스트
        """
        # 사용자 메시지 추가
        self.messages.append(HumanMessage(content=user_input))

        # 에이전트 실행
        result = self.graph.invoke({"messages": self.messages})

        # 결과에서 메시지 업데이트
        self.messages = result["messages"]

        # 마지막 AI 메시지 반환
        for msg in reversed(self.messages):
            if isinstance(msg, AIMessage):
                return msg.content

        return "응답을 생성하지 못했습니다."

    def stream_chat(self, user_input: str):
        """스트리밍 방식으로 사용자 입력 처리

        Args:
            user_input: 사용자 메시지

        Yields:
            에이전트 이벤트 (도구 호출, 응답 등)
        """
        self.messages.append(HumanMessage(content=user_input))

        for event in self.graph.stream({"messages": self.messages}):
            yield event

            # 메시지 업데이트
            if "agent" in event:
                agent_messages = event["agent"].get("messages", [])
                for msg in agent_messages:
                    if msg not in self.messages:
                        self.messages.append(msg)
            elif "tools" in event:
                tool_messages = event["tools"].get("messages", [])
                for msg in tool_messages:
                    if msg not in self.messages:
                        self.messages.append(msg)

    def reset(self):
        """대화 히스토리 초기화"""
        self.messages = []
