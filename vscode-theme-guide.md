# VS Code 코드 색상 개선 가이드

## 빠른 해결법

### 1. Python 확장 설치 확인

```bash
# 터미널에서 실행
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
```

### 2. VS Code 재시작

`Cmd/Ctrl + Shift + P` → "Developer: Reload Window"

### 3. Python 인터프리터 선택

`Cmd/Ctrl + Shift + P` → "Python: Select Interpreter" → `.venv` 선택

## 인기 테마 추천

### 다크 테마 (어두운 배경)

#### 1. **GitHub Dark** (추천)

```bash
code --install-extension GitHub.github-vscode-theme
```

- 깔끔하고 눈이 편안함
- GitHub 스타일의 친숙한 색상

#### 2. **One Dark Pro**

```bash
code --install-extension zhuangtongfa.material-theme
```

- Atom 에디터의 인기 테마
- 변수와 함수가 잘 구분됨

#### 3. **Dracula**

```bash
code --install-extension dracula-theme.theme-dracula
```

- 보라색 계열의 독특한 색상
- 주석과 문자열이 잘 보임

#### 4. **Tokyo Night**

```bash
code --install-extension enkia.tokyo-night
```

- 부드러운 색상 조합
- 장시간 코딩에 좋음

### 라이트 테마 (밝은 배경)

#### 1. **GitHub Light**

```bash
code --install-extension GitHub.github-vscode-theme
```

#### 2. **Atom One Light**

```bash
code --install-extension akamud.vscode-theme-onelight
```

## 테마 적용 방법

### 방법 1: 명령 팔레트

1. `Cmd/Ctrl + Shift + P`
2. "Preferences: Color Theme" 입력
3. 원하는 테마 선택

### 방법 2: 설정

1. `Cmd/Ctrl + ,` (설정 열기)
2. "Color Theme" 검색
3. 드롭다운에서 선택

### 방법 3: 빠른 전환

`Cmd/Ctrl + K` → `Cmd/Ctrl + T`

## 색상 문제 해결

### 변수가 흰색으로만 보일 때

1. Pylance 설치 확인:

```bash
code --install-extension ms-python.vscode-pylance
```

2. 설정에서 Semantic Highlighting 활성화:

```json
{
  "editor.semanticHighlighting.enabled": true,
  "python.languageServer": "Pylance"
}
```

### 특정 색상 직접 수정

`.vscode/settings.json`에서:

```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "variable.other.python",
        "settings": {
          "foreground": "#9CDCFE" // 하늘색 변수
        }
      },
      {
        "scope": "entity.name.function.python",
        "settings": {
          "foreground": "#DCDCAA" // 노란색 함수
        }
      }
    ]
  }
}
```

## 추가 색상 강화

### 1. Bracket Pair Colorizer

```bash
code --install-extension CoenraadS.bracket-pair-colorizer-2
```

- 괄호를 색상으로 구분

### 2. Indent Rainbow

```bash
code --install-extension oderwat.indent-rainbow
```

- 들여쓰기를 색상으로 표시

### 3. Color Highlight

```bash
code --install-extension naumovs.color-highlight
```

- 색상 코드를 실제 색으로 표시

## 폰트 추천

### 1. Fira Code (프로그래밍 전용)

- 다운로드: https://github.com/tonsky/FiraCode
- 특징: 프로그래밍 리가처 지원 (=> 가 ⇒로 표시)

### 2. JetBrains Mono

- 다운로드: https://www.jetbrains.com/lp/mono/
- 특징: 가독성 최적화

### 폰트 설정

```json
{
  "editor.fontFamily": "Fira Code, Menlo, Monaco, monospace",
  "editor.fontLigatures": true,
  "editor.fontSize": 14
}
```

## 현재 프로젝트 설정

이미 `.vscode/settings.json`에 다음 설정이 적용되어 있습니다:

- ✅ Semantic Highlighting 활성화
- ✅ Bracket Pair Colorization 활성화
- ✅ 변수, 함수, 클래스 색상 커스터마이징
- ✅ GitHub Dark Default 테마 설정

**VS Code를 재시작하면 색상이 제대로 표시됩니다!**

## 테마 미리보기 사이트

- https://vscodethemes.com/
- https://marketplace.visualstudio.com/search?target=VSCode&category=Themes
