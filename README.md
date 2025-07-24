# AI 모노레포

uv를 사용한 파이썬 AI 프로젝트 모노레포입니다.

## 구조

```
ai/
├── packages/
│   ├── book-recommender/     # 책 추천 시스템
│   ├── chat_model/          # 챗봇 모델 예제
│   ├── langchain/           # LangChain 예제
│   ├── openai-cookbook/     # OpenAI API 쿡북
│   ├── rag-1/              # RAG 튜토리얼
│   └── rag-project/        # RAG 프로젝트
└── pyproject.toml          # 워크스페이스 설정
```

## 시작하기

### 1. uv 설치

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew
brew install uv
```

### 2. 의존성 설치

```bash
# 워크스페이스의 모든 의존성 설치
uv sync

# 특정 패키지만 설치
uv sync --package book-recommender
```

### 3. 개발 도구

```bash
# 코드 포맷팅
uv run black .

# 린팅
uv run ruff check .

# 타입 체크
uv run mypy .

# 테스트 실행
uv run pytest
```

## 패키지별 실행

### book-recommender

```bash
cd packages/book-recommender
uv run python gradio-dashboard.py
```

### chat_model

```bash
cd packages/chat_model
uv run python 1_chat_model_basic.py
```

### rag 튜토리얼

```bash
cd packages/rag-1
uv run python 1a_rag_basics.py
```

## 새 패키지 추가

1. `packages/` 디렉토리에 새 폴더 생성
2. `pyproject.toml` 파일 생성
3. `uv sync` 실행

## 의존성 관리

### 패키지별 의존성 추가

```bash
cd packages/your-package
uv add numpy pandas
```

### 개발 의존성 추가 (전체 워크스페이스)

```bash
uv add --dev pytest-cov
```

## Jupyter 노트북 사용

```bash
# Jupyter Lab 실행
uv run jupyter lab

# 특정 노트북 실행
uv run jupyter notebook packages/book-recommender/data-exploration.ipynb
```

## 환경 변수

각 패키지에 `.env` 파일을 생성하여 API 키 등을 관리하세요:

```bash
# packages/your-package/.env
OPENAI_API_KEY=your-api-key
```

## 문제 해결

### 의존성 충돌

```bash
# 의존성 재설치
uv sync --refresh
```

### 캐시 정리

```bash
uv cache clean
```
