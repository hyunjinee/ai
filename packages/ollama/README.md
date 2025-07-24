# Ollama Examples

Ollama API를 사용하는 Python 예제 모음입니다.

## 파일 설명

- `start-1.py`: Ollama REST API를 직접 사용하는 예제 (requests 라이브러리)
- `start-2.py`: Ollama Python 라이브러리를 사용하는 예제

## 사전 준비

1. Ollama 설치

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# https://ollama.com에서 다운로드
```

2. 모델 다운로드

```bash
ollama pull llama3.2
```

3. Ollama 서버 실행

```bash
ollama serve
```

## 실행 방법

### 프로젝트 루트에서 실행

```bash
# REST API 예제 실행
uv run python packages/ollama/start-1.py

# Python 라이브러리 예제 실행
uv run python packages/ollama/start-2.py
```

### 패키지 디렉토리에서 실행

```bash
cd packages/ollama

# REST API 예제
uv run python start-1.py

# Python 라이브러리 예제
uv run python start-2.py
```

## 예제 내용

### start-1.py

- Ollama REST API 직접 호출
- 스트리밍 응답 처리
- HTTP POST 요청으로 텍스트 생성

### start-2.py

- Ollama Python 라이브러리 사용
- 채팅 예제 (일반 및 스트리밍)
- 텍스트 생성 예제
- 커스텀 모델 생성 및 삭제
- 시스템 프롬프트 설정

## 주요 기능

1. **텍스트 생성**: 프롬프트를 입력하여 텍스트 생성
2. **채팅**: 대화형 인터페이스로 질문과 답변
3. **모델 관리**: 커스텀 모델 생성, 설정, 삭제
4. **스트리밍**: 실시간으로 생성되는 텍스트 확인

## 문제 해결

### Ollama 서버 연결 실패

```bash
# Ollama 서버 상태 확인
ollama list

# 서버 재시작
ollama serve
```

### 모델을 찾을 수 없음

```bash
# 사용 가능한 모델 확인
ollama list

# 모델 다운로드
ollama pull llama3.2
```
