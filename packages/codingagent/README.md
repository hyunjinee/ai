# hyunjin 🤖

커맨드라인에서 동작하는 AI 코딩 에이전트. Claude Code처럼 자연어로 코드를 작성, 수정, 분석할 수 있다.

## 기능

- 📄 **파일 읽기/쓰기**: 코드 파일 생성 및 수정
- 🔧 **코드 편집**: 특정 부분만 정확하게 수정
- 📁 **디렉토리 탐색**: 프로젝트 구조 파악
- 🔍 **파일 검색**: 이름 또는 내용으로 파일 검색
- 💻 **터미널 명령 실행**: 빌드, 테스트, 패키지 설치 등

## 설치

```bash
cd packages/codingagent
uv sync
```

## 환경 설정

OpenAI API 키가 필요하다:

```bash
export OPENAI_API_KEY='sk-...'
```

또는 `.env` 파일 생성:

```env
OPENAI_API_KEY=sk-...
```

## 사용법

### 원샷 모드 (Claude Code 스타일)

```bash
# 바로 질문하고 답변 받기
hyunjin "현재 디렉토리의 파일 목록을 보여줘"

# 실행 후 대화형 모드로 계속
hyunjin -c "main.py 파일을 분석해줘"

# 다른 모델 사용
hyunjin -m gpt-4o-mini "hello.py 만들어줘"
```

### 대화형 모드

```bash
# 인자 없이 실행하면 대화형 모드
hyunjin
```

## CLI 옵션

```
usage: hyunjin [-h] [-m MODEL] [-c] [prompt]

positional arguments:
  prompt                실행할 프롬프트 (없으면 대화형 모드)

options:
  -h, --help            도움말
  -m MODEL, --model MODEL
                        사용할 모델 (기본: gpt-4o)
  -c, --continue        원샷 실행 후 대화형 모드로 계속
```

## 대화형 모드 명령어

| 명령어            | 설명                    |
| ----------------- | ----------------------- |
| `/help`           | 도움말 표시             |
| `/clear`          | 대화 히스토리 초기화    |
| `/exit`           | 프로그램 종료           |
| `/model <모델명>` | 사용할 모델 변경        |
| `/cd <경로>`      | 작업 디렉토리 변경      |
| `/pwd`            | 현재 작업 디렉토리 표시 |

## 사용 예시

```bash
$ hyunjin "tests 폴더에서 test_로 시작하는 파일들 찾아줘"

> tests 폴더에서 test_로 시작하는 파일들 찾아줘

🔧 도구 호출
  search_files
  pattern: test_
  directory: tests

📋 결과
  검색 결과 (3개):
  test_api.py
  test_models.py
  test_utils.py

🤖 응답
tests 폴더에서 test_로 시작하는 파일 3개를 찾았습니다...
```

```bash
$ hyunjin

╔═══════════════════════════════════════════════════════════════╗
║   🤖  hyunjin  - AI 코딩 에이전트                             ║
╚═══════════════════════════════════════════════════════════════╝

hyunjin > hello.py 파일을 만들어서 "Hello, World!"를 출력해줘

🔧 도구 호출
  write_file
  file_path: hello.py
  content: print("Hello, World!")

📋 결과
  Success: 파일 작성 완료 - /path/to/hello.py

🤖 응답
hello.py 파일을 생성했습니다.
```

## 사용 가능한 모델

- `gpt-4o` (기본값) - 가장 강력한 코딩 능력
- `gpt-4o-mini` - 더 빠르고 저렴
- `gpt-4-turbo` - 안정적인 성능

## 프로젝트 구조

```
codingagent/
├── pyproject.toml      # 프로젝트 설정 및 의존성
├── README.md
└── src/
    ├── __init__.py
    ├── main.py         # CLI 엔트리포인트
    ├── agent.py        # LangGraph 에이전트 로직
    └── tools.py        # 도구 정의 (파일, 터미널 등)
```

## 기술 스택

- **LangGraph**: 에이전트 오케스트레이션
- **LangChain**: LLM 추상화 및 도구 바인딩
- **OpenAI GPT-4o**: 코드 생성 및 추론
- **Rich**: 터미널 UI
- **prompt-toolkit**: 입력 히스토리 및 자동완성

## 향후 계획

- [ ] 멀티 파일 리팩토링 지원
- [ ] Git 통합 (commit, diff 등)
- [ ] 코드 리뷰 기능
- [ ] 로컬 LLM 지원 (Ollama)
- [ ] 프로젝트 컨텍스트 자동 인식
