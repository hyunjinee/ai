# 코드 저장 시 자동 포매팅 설정 가이드

## VS Code (Visual Studio Code)

### 1. 필수 확장 프로그램 설치

```bash
# VS Code 터미널에서 실행
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
code --install-extension ms-python.isort
```

### 2. 설정 적용

`.vscode/settings.json` 파일이 이미 생성되어 있습니다:

- ✅ 저장 시 Black 자동 실행
- ✅ import 자동 정렬
- ✅ 후행 공백 제거
- ✅ 파일 끝 개행 추가

### 3. 포매터 선택

`Cmd/Ctrl + Shift + P` → "Format Document With..." 선택:

- **Black** (권장): 표준 Python 포매터
- **Ruff**: 더 빠른 대안

## PyCharm / IntelliJ IDEA

### 1. Black 설정

```
Preferences → Tools → External Tools → +
- Name: Black
- Program: $PyInterpreterDirectory$/black
- Arguments: $FilePath$
- Working directory: $ProjectFileDir$
```

### 2. 저장 시 자동 실행

```
Preferences → Tools → Actions on Save
- ✅ Reformat code
- ✅ Optimize imports
- ✅ Run External Tools: Black
```

### 3. 단축키 설정

```
Preferences → Keymap
- External Tools → Black → 우클릭
- Add Keyboard Shortcut: Cmd/Ctrl + S
```

## Neovim / Vim

### 1. 플러그인 설치 (vim-plug 사용)

```vim
" ~/.config/nvim/init.vim 또는 ~/.vimrc
Plug 'psf/black', { 'branch': 'stable' }
Plug 'fisadev/vim-isort'
```

### 2. 자동 포매팅 설정

```vim
" 저장 시 자동 포맷
autocmd BufWritePre *.py execute ':Black'
autocmd BufWritePre *.py execute ':Isort'

" 또는 null-ls/none-ls 사용 (Neovim)
require("null-ls").setup({
    sources = {
        require("null-ls").builtins.formatting.black,
        require("null-ls").builtins.formatting.isort,
    },
    on_attach = function(client, bufnr)
        vim.api.nvim_create_autocmd("BufWritePre", {
            buffer = bufnr,
            callback = function()
                vim.lsp.buf.format({ async = false })
            end,
        })
    end,
})
```

## Sublime Text

### 1. Package Control에서 설치

- `Cmd/Ctrl + Shift + P` → "Package Control: Install Package"
- 설치: `Python Black`, `SublimeLinter`, `AutoPEP8`

### 2. 설정 추가

```json
// Preferences → Package Settings → Python Black → Settings
{
  "black_on_save": true,
  "black_line_length": 88,
  "black_fast": true
}
```

## Cursor

### 1. 설정

Cursor는 VS Code 기반이므로 동일한 설정 사용:

- `.vscode/settings.json` 파일이 자동으로 적용됨
- 동일한 확장 프로그램 사용 가능

### 2. AI 지원 포매팅

```
설정 → AI → Code Formatting
- ✅ Format on save with AI suggestions
```

## 터미널에서 수동 실행

### 개별 파일

```bash
# Black
uv run black file.py

# Ruff (더 빠름)
uv run ruff format file.py

# isort
uv run isort file.py
```

### 전체 프로젝트

```bash
# 권장 워크플로우
uv run isort . && uv run black .

# 또는 Ruff로 한번에
uv run ruff check --fix . && uv run ruff format .
```

## Pre-commit Hook 설정

### 1. 설치

```bash
uv add --dev pre-commit
```

### 2. `.pre-commit-config.yaml` 생성

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format
```

### 3. 활성화

```bash
uv run pre-commit install
```

이제 git commit 시 자동으로 포매팅됩니다.

## 문제 해결

### VS Code에서 포매터가 작동하지 않을 때

1. Python 인터프리터 확인: `Cmd/Ctrl + Shift + P` → "Python: Select Interpreter"
2. `.venv` 선택 확인
3. 확장 프로그램 재설치

### Black과 다른 포매터 충돌

```json
// .vscode/settings.json에 추가
"python.formatting.provider": "none",  // 기본 포매터 비활성화
"[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"  // Black만 사용
}
```

### 특정 파일/라인 제외

```python
# fmt: off
이_코드는_포매팅_안됨 = {"복잡한": "구조"}
# fmt: on

# isort: skip
import 정렬하지_않을_import
```

## 권장 설정 요약

1. **VS Code + Black + Ruff**: 가장 인기 있는 조합
2. **저장 시 자동 실행**: 일관성 유지
3. **Pre-commit**: 팀 협업 시 필수
4. **Line length 88**: Black 기본값 사용

현재 프로젝트는 이미 모든 설정이 완료되어 있습니다!
VS Code를 재시작하면 저장할 때마다 자동으로 포매팅됩니다.
