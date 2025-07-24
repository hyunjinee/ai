# uv 완벽 가이드

## 목차

1. [uv란?](#uv란)
2. [설치](#설치)
3. [기본 개념](#기본-개념)
4. [프로젝트 관리](#프로젝트-관리)
5. [의존성 관리](#의존성-관리)
6. [가상환경 관리](#가상환경-관리)
7. [모노레포 설정](#모노레포-설정)
8. [스크립트 실행](#스크립트-실행)
9. [고급 기능](#고급-기능)
10. [팁과 모범 사례](#팁과-모범-사례)
11. [문제 해결](#문제-해결)
12. [마이그레이션 가이드](#마이그레이션-가이드)

## uv란?

uv는 Rust로 작성된 초고속 Python 패키지 및 프로젝트 매니저입니다. pip, pip-tools, pipx, poetry, pyenv, virtualenv 등의 기능을 하나의 도구로 통합했습니다.

### 주요 특징

- **초고속**: Rust로 작성되어 기존 도구보다 10-100배 빠름
- **올인원**: 패키지 관리, 가상환경, Python 버전 관리 통합
- **표준 준수**: PEP 표준을 엄격히 따름
- **드롭인 대체**: pip와 호환되는 인터페이스
- **크로스 플랫폼**: Windows, macOS, Linux 지원

## 설치

### macOS/Linux

```bash
# 공식 설치 스크립트
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew
brew install uv

# pipx
pipx install uv
```

### Windows

```powershell
# PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Scoop
scoop install uv

# Cargo
cargo install --git https://github.com/astral-sh/uv uv
```

### 설치 확인

```bash
uv --version
```

## 기본 개념

### uv의 작동 방식

1. **프로젝트 중심**: `pyproject.toml`을 중심으로 프로젝트 관리
2. **자동 가상환경**: 프로젝트마다 자동으로 `.venv` 생성
3. **잠금 파일**: `uv.lock`으로 재현 가능한 환경 보장
4. **캐싱**: 글로벌 캐시로 디스크 공간 절약

### 주요 명령어 체계

```bash
uv [명령어] [옵션]
uv pip [pip 명령어]  # pip 호환 모드
uv run [명령어]      # 가상환경에서 실행
```

## 프로젝트 관리

### 새 프로젝트 생성

```bash
# 기본 프로젝트 생성
uv init my-project
cd my-project

# 특정 Python 버전으로 생성
uv init --python 3.11 my-project

# 라이브러리 템플릿 사용
uv init --lib my-library

# 애플리케이션 템플릿 사용
uv init --app my-app
```

### 프로젝트 구조

```
my-project/
├── pyproject.toml    # 프로젝트 설정
├── uv.lock          # 잠금 파일 (자동 생성)
├── .venv/           # 가상환경 (자동 생성)
├── src/             # 소스 코드
└── README.md
```

### pyproject.toml 예시

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "프로젝트 설명"
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
    "pandas>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 의존성 관리

### 의존성 추가

```bash
# 프로덕션 의존성 추가
uv add requests pandas numpy

# 개발 의존성 추가
uv add --dev pytest black ruff

# 특정 버전 지정
uv add "django>=4.2,<5.0"

# 로컬 패키지 추가
uv add --editable ./local-package

# Git 저장소에서 설치
uv add git+https://github.com/user/repo.git

# 추가 기능과 함께 설치
uv add "fastapi[all]"
```

### 의존성 제거

```bash
# 패키지 제거
uv remove requests

# 개발 의존성 제거
uv remove --dev pytest
```

### 의존성 업데이트

```bash
# 모든 패키지 업데이트
uv sync --upgrade

# 특정 패키지만 업데이트
uv sync --upgrade-package requests

# 잠금 파일 재생성
uv lock --upgrade
```

### 의존성 확인

```bash
# 설치된 패키지 목록
uv pip list

# 의존성 트리 보기
uv pip show package-name

# 오래된 패키지 확인
uv pip list --outdated
```

## 가상환경 관리

### 자동 가상환경

```bash
# uv는 자동으로 .venv 생성 및 활성화
uv sync  # 가상환경 생성 및 의존성 설치
```

### 수동 가상환경 관리

```bash
# 가상환경 생성
uv venv

# 특정 Python 버전으로 생성
uv venv --python 3.11

# 커스텀 경로에 생성
uv venv /path/to/venv

# 가상환경 활성화 (수동)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Python 버전 관리

```bash
# 사용 가능한 Python 버전 확인
uv python list

# Python 설치
uv python install 3.11

# 프로젝트에 Python 버전 고정
uv python pin 3.11
```

## 모노레포 설정

### 워크스페이스 구성

```toml
# 루트 pyproject.toml
[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[tool.uv.workspace]
members = ["packages/*"]
```

### 패키지 구조

```
monorepo/
├── pyproject.toml       # 워크스페이스 설정
├── packages/
│   ├── package-a/
│   │   └── pyproject.toml
│   └── package-b/
│       └── pyproject.toml
└── uv.lock             # 통합 잠금 파일
```

### 워크스페이스 명령어

```bash
# 전체 워크스페이스 동기화
uv sync

# 특정 패키지만 동기화
uv sync --package package-a

# 워크스페이스 의존성 추가
uv add --dev pytest  # 전체 워크스페이스
cd packages/package-a && uv add requests  # 특정 패키지
```

## 스크립트 실행

### uv run 사용

```bash
# Python 스크립트 실행
uv run python script.py

# 모듈 실행
uv run -m pytest

# 설치된 명령어 실행
uv run black .
uv run jupyter lab

# 인라인 스크립트 실행
uv run python -c "print('Hello, uv!')"
```

### 스크립트 의존성

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "pandas",
# ]
# ///

import requests
import pandas as pd

# 스크립트 코드...
```

실행:

```bash
uv run script.py  # 자동으로 의존성 설치
```

## 고급 기능

### 환경 변수

```bash
# UV 관련 환경 변수
export UV_CACHE_DIR=/custom/cache/path
export UV_INDEX_URL=https://custom.pypi.org/simple
export UV_EXTRA_INDEX_URL=https://extra.pypi.org/simple
export UV_NO_CACHE=1  # 캐시 비활성화
```

### 설정 파일

```toml
# pyproject.toml 또는 uv.toml
[tool.uv]
index-url = "https://custom.pypi.org/simple"
extra-index-url = ["https://extra.pypi.org/simple"]
find-links = ["https://download.pytorch.org/whl/torch_stable.html"]
no-binary = ["numpy"]  # 소스에서 빌드
```

### pip 호환 모드

```bash
# pip 명령어를 uv로 대체
uv pip install requests
uv pip uninstall requests
uv pip freeze > requirements.txt
uv pip install -r requirements.txt
```

### 캐시 관리

```bash
# 캐시 정보 확인
uv cache dir
uv cache info

# 캐시 정리
uv cache clean
uv cache clean package-name

# 캐시 비우기
uv cache prune
```

### 컴파일된 요구사항

```bash
# requirements.in에서 requirements.txt 생성
uv pip compile requirements.in -o requirements.txt

# 업그레이드하며 컴파일
uv pip compile --upgrade requirements.in -o requirements.txt

# 플랫폼별 컴파일
uv pip compile --platform linux requirements.in
```

## 팁과 모범 사례

### 1. 프로젝트 구조화

```
project/
├── pyproject.toml      # 프로젝트 메타데이터
├── uv.lock            # 버전 잠금 (커밋에 포함)
├── .venv/             # 가상환경 (gitignore)
├── src/               # 소스 코드
│   └── my_package/
├── tests/             # 테스트
├── docs/              # 문서
└── scripts/           # 유틸리티 스크립트
```

### 2. CI/CD 설정

```yaml
# GitHub Actions 예시
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
      - run: uv sync
      - run: uv run pytest
```

### 3. 도커 이미지 최적화

```dockerfile
# 멀티 스테이지 빌드
FROM ghcr.io/astral-sh/uv:latest as builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

FROM python:3.11-slim
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "app.py"]
```

### 4. 개발 워크플로우

```bash
# 프로젝트 설정
uv init my-project
cd my-project

# 의존성 추가
uv add fastapi uvicorn
uv add --dev pytest black ruff

# 개발 서버 실행
uv run uvicorn main:app --reload

# 테스트 실행
uv run pytest

# 코드 포맷팅
uv run black .
uv run ruff check --fix .
```

### 5. 성능 최적화

- 글로벌 캐시 활용: 동일 패키지 재다운로드 방지
- `--frozen` 플래그: 프로덕션에서 lock 파일 엄격히 따르기
- 병렬 설치: uv는 자동으로 병렬 처리
- 인덱스 URL 최적화: 가까운 미러 사용

## 문제 해결

### 일반적인 문제

#### 1. 가상환경 활성화 문제

```bash
# uv run을 사용하면 자동 활성화
uv run python script.py

# 수동 활성화가 필요한 경우
source .venv/bin/activate  # bash/zsh
. .venv/bin/activate       # sh
.venv\Scripts\activate     # Windows
```

#### 2. 의존성 충돌

```bash
# 상세한 해결 과정 보기
uv sync -v

# 잠금 파일 재생성
rm uv.lock
uv lock

# 특정 패키지 버전 강제
uv add "package==1.2.3"
```

#### 3. 캐시 문제

```bash
# 캐시 정리
uv cache clean

# 캐시 없이 설치
uv sync --no-cache
```

#### 4. Python 버전 문제

```bash
# Python 버전 확인
uv run python --version

# 특정 버전 사용
uv venv --python 3.11
uv python pin 3.11
```

### 디버깅 옵션

```bash
# 상세 로그
uv -v sync
uv -vv sync  # 더 상세한 로그

# 드라이런
uv sync --dry-run

# 의존성 해결 과정 보기
uv lock -v
```

## 마이그레이션 가이드

### pip/requirements.txt에서 마이그레이션

```bash
# 1. uv 초기화
uv init .

# 2. requirements.txt 임포트
uv pip install -r requirements.txt

# 3. pyproject.toml에 의존성 추가
uv add $(cat requirements.txt | grep -v '^#' | cut -d'=' -f1)

# 4. lock 파일 생성
uv lock
```

### Poetry에서 마이그레이션

```bash
# 1. poetry.lock 내보내기
poetry export -f requirements.txt > requirements.txt

# 2. uv 프로젝트 초기화
uv init .

# 3. 의존성 설치
uv pip install -r requirements.txt

# 4. pyproject.toml 수동 편집
# Poetry의 [tool.poetry.dependencies]를 [project.dependencies]로 변경
```

### Pipenv에서 마이그레이션

```bash
# 1. requirements.txt 생성
pipenv requirements > requirements.txt
pipenv requirements --dev > requirements-dev.txt

# 2. uv 초기화 및 설치
uv init .
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt
```

### 모범 사례 체크리스트

- [ ] `uv.lock` 파일을 버전 관리에 포함
- [ ] `.venv/`를 `.gitignore`에 추가
- [ ] CI/CD에서 `uv sync --frozen` 사용
- [ ] 정기적으로 `uv sync --upgrade` 실행
- [ ] 프로덕션과 개발 의존성 분리
- [ ] Python 버전을 `pyproject.toml`에 명시
- [ ] 캐시 디렉토리를 SSD에 위치
- [ ] 모노레포의 경우 워크스페이스 활용

## 추가 리소스

- [공식 문서](https://github.com/astral-sh/uv)
- [uv 블로그](https://astral.sh/blog)
- [PyPI 프로젝트](https://pypi.org/project/uv/)
- [GitHub 이슈](https://github.com/astral-sh/uv/issues)
- [Discord 커뮤니티](https://discord.gg/astral-sh)
