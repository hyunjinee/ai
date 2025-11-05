# AI SDK Examples

AI SDK를 사용한 다양한 예시 코드 모음입니다.

## 설치

```bash
pnpm install
```

## 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API 키를 입력하세요:

```bash
cp .env.example .env
```

## 실행

```bash
# 개발 모드 (watch mode)
pnpm dev

# 일반 실행
pnpm start
```

## 지원하는 Provider

- OpenAI (GPT-4, GPT-3.5, etc.)
- Anthropic (Claude)
- Google (Gemini)
- xAI (Grok)

## 예시 코드

- `src/index.ts` - 기본 예시
- `src/foundations/` - AI SDK 기초 개념
- `src/core/` - AI SDK Core 예시
- `src/ui/` - AI SDK UI 예시

## 참고 자료

- [AI SDK 공식 문서](https://ai-sdk.dev/)
- [AI SDK GitHub](https://github.com/vercel/ai)

