"""
hyunjin - AI 코딩 에이전트 CLI
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from h.agent import CodingAgent, OLLAMA_PREFIX, OLLAMA_MODELS

# 환경 변수 로드
load_dotenv()

# Rich 콘솔
console = Console()

# 프롬프트 스타일
prompt_style = Style.from_dict(
    {
        "prompt": "#00aa00 bold",
    }
)

# 히스토리 파일 경로
HISTORY_FILE = Path.home() / ".h_agent_history"


def print_banner():
    """시작 배너 출력"""
    banner = """
╔═══════════════════════════════════════════════════╗
║                                                   ║
║   🤖  h  - AI 코딩 에이전트                       ║
║                                                   ║
║   /help - 도움말  /exit - 종료  /model - 모델    ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
"""
    console.print(banner, style="cyan")


def print_help():
    """도움말 출력"""
    ollama_models_str = ", ".join(OLLAMA_MODELS[:3])
    help_text = f"""
## 사용법

자연어로 코딩 관련 요청을 입력하세요.

### 예시

- "현재 디렉토리의 파일 목록을 보여줘"
- "hello.py 파일을 만들어서 Hello World를 출력하는 코드를 작성해줘"
- "main.py 파일을 읽고 버그가 있는지 확인해줘"
- "tests 폴더에서 test_로 시작하는 파일들을 찾아줘"
- "pip list 명령을 실행해서 설치된 패키지를 확인해줘"

### 명령어

| 명령어 | 설명 |
|--------|------|
| `/help` | 이 도움말 표시 |
| `/clear` | 대화 히스토리 초기화 |
| `/exit`, `/quit`, `/q` | 프로그램 종료 |
| `/model <모델명>` | 사용할 모델 변경 |
| `/models` | 사용 가능한 모델 목록 표시 |
| `/cd <경로>` | 작업 디렉토리 변경 |
| `/pwd` | 현재 작업 디렉토리 표시 |

### 모델 사용법

- **OpenAI**: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`
- **Ollama**: `ollama:모델명` (예: `ollama:qwen2.5-coder:14b`)

추천 Ollama 모델: {ollama_models_str}
"""
    console.print(Markdown(help_text))


def format_tool_call(tool_name: str, tool_input: dict) -> Panel:
    """도구 호출 포맷팅"""
    input_str = "\n".join(f"  {k}: {v}" for k, v in tool_input.items())
    return Panel(
        f"[bold]{tool_name}[/bold]\n{input_str}",
        title="🔧 도구 호출",
        border_style="yellow",
    )


def format_tool_result(result: str) -> Panel:
    """도구 결과 포맷팅"""
    # 결과가 너무 길면 잘라내기
    max_len = 2000
    if len(result) > max_len:
        result = result[:max_len] + f"\n... ({len(result) - max_len}자 생략)"

    return Panel(result, title="📋 결과", border_style="green")


def run_agent_streaming(agent: CodingAgent, user_input: str):
    """스트리밍 방식으로 에이전트 실행"""
    console.print()

    final_response = ""

    for event in agent.stream_chat(user_input):
        if "agent" in event:
            messages = event["agent"].get("messages", [])
            for msg in messages:
                if isinstance(msg, AIMessage):
                    # 도구 호출 표시
                    if msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            console.print(
                                format_tool_call(tool_call["name"], tool_call["args"])
                            )
                    # 텍스트 응답
                    if msg.content:
                        final_response = msg.content

        elif "tools" in event:
            messages = event["tools"].get("messages", [])
            for msg in messages:
                if isinstance(msg, ToolMessage):
                    console.print(format_tool_result(msg.content))

    # 최종 응답 출력
    if final_response:
        console.print()
        console.print(Panel(Markdown(final_response), title="🤖 응답", border_style="blue"))


def parse_args():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        prog="h",
        description="AI 코딩 에이전트 - 자연어로 코드를 작성하고 수정",
        epilog="예: h '현재 디렉토리의 파일 목록을 보여줘'",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="실행할 프롬프트 (없으면 대화형 모드)",
    )
    parser.add_argument(
        "-m", "--model",
        default="gpt-4o",
        help="사용할 모델 (기본: gpt-4o, Ollama: ollama:모델명)",
    )
    parser.add_argument(
        "-c", "--continue",
        dest="continue_chat",
        action="store_true",
        help="원샷 실행 후 대화형 모드로 계속",
    )
    return parser.parse_args()


def run_oneshot(agent: CodingAgent, prompt: str):
    """원샷 모드 - 하나의 프롬프트 실행 후 종료"""
    console.print(f"[dim]> {prompt}[/dim]\n")
    run_agent_streaming(agent, prompt)


def run_interactive(agent: CodingAgent, model_name: str):
    """대화형 모드 - REPL"""
    print_banner()
    console.print(f"[dim]현재 디렉토리: {os.getcwd()}[/dim]")
    console.print(f"[dim]모델: {model_name}[/dim]")
    console.print()

    session = PromptSession(history=FileHistory(str(HISTORY_FILE)))

    while True:
        try:
            user_input = session.prompt(
                [("class:prompt", "h > ")],
                style=prompt_style,
            ).strip()

            if not user_input:
                continue

            # 명령어 처리
            if user_input.startswith("/"):
                cmd_parts = user_input.split(maxsplit=1)
                cmd = cmd_parts[0].lower()
                arg = cmd_parts[1] if len(cmd_parts) > 1 else ""

                if cmd in ["/exit", "/quit", "/q"]:
                    console.print("[yellow]안녕히 가세요! 👋[/yellow]")
                    break

                elif cmd == "/help":
                    print_help()

                elif cmd == "/clear":
                    agent.reset()
                    console.print("[green]대화 히스토리가 초기화되었습니다.[/green]")

                elif cmd == "/model":
                    if arg:
                        model_name = arg
                        agent = CodingAgent(model_name=model_name)
                        console.print(f"[green]모델이 {model_name}로 변경되었습니다.[/green]")
                    else:
                        console.print(f"[blue]현재 모델: {model_name}[/blue]")
                        console.print("사용법: /model <모델명>")
                        console.print("예: /model gpt-4o-mini")
                        console.print("예: /model ollama:qwen2.5-coder:14b")

                elif cmd == "/models":
                    console.print("[bold]사용 가능한 모델:[/bold]\n")
                    console.print("[cyan]OpenAI:[/cyan]")
                    console.print("  • gpt-4o (기본)")
                    console.print("  • gpt-4o-mini")
                    console.print("  • gpt-4-turbo")
                    console.print()
                    console.print("[cyan]Ollama (로컬):[/cyan]")
                    for m in OLLAMA_MODELS:
                        console.print(f"  • ollama:{m}")
                    console.print()
                    console.print("[dim]Ollama 사용: ollama:모델명 형식으로 지정[/dim]")

                elif cmd == "/cd":
                    if arg:
                        try:
                            os.chdir(os.path.expanduser(arg))
                            console.print(f"[green]작업 디렉토리 변경: {os.getcwd()}[/green]")
                        except Exception as e:
                            console.print(f"[red]Error: {e}[/red]")
                    else:
                        console.print("사용법: /cd <경로>")

                elif cmd == "/pwd":
                    console.print(f"[blue]{os.getcwd()}[/blue]")

                else:
                    console.print(f"[red]알 수 없는 명령어: {cmd}[/red]")
                    console.print("/help 를 입력해 도움말을 확인하세요.")

                continue

            run_agent_streaming(agent, user_input)

        except KeyboardInterrupt:
            console.print("\n[yellow]Ctrl+C - 종료하려면 /exit 를 입력하세요.[/yellow]")
        except EOFError:
            console.print("\n[yellow]안녕히 가세요! 👋[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")


def main():
    """메인 함수"""
    args = parse_args()

    # Ollama 모델이 아닌 경우 OpenAI API 키 확인
    if not args.model.startswith(OLLAMA_PREFIX):
        if not os.environ.get("OPENAI_API_KEY"):
            console.print(
                "[red]Error: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.[/red]"
            )
            console.print("export OPENAI_API_KEY='your-api-key' 명령으로 설정하세요.")
            console.print("[dim]또는 Ollama 모델 사용: hyunjin -m ollama:qwen2.5-coder:14b[/dim]")
            sys.exit(1)

    # 에이전트 초기화
    agent = CodingAgent(model_name=args.model)

    if args.prompt:
        # 원샷 모드
        run_oneshot(agent, args.prompt)

        # -c 옵션이 있으면 대화형 모드로 계속
        if args.continue_chat:
            console.print()
            run_interactive(agent, args.model)
    else:
        # 대화형 모드
        run_interactive(agent, args.model)


if __name__ == "__main__":
    main()
