import "dotenv/config"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"
import { anthropic } from "@ai-sdk/anthropic"
import { google } from "@ai-sdk/google"
import { xai } from "@ai-sdk/xai"

/**
 * 다양한 Foundation Model로 텍스트 생성하기
 *
 * AI SDK는 여러 AI 제공업체를 통합하여 동일한 인터페이스로 사용할 수 있습니다.
 * LLM은 추론 엔진이기 때문에 그 뒤에 올 가능성이 가장 높은 단어를 예측합니다.
 *
 * @see https://ai-sdk.dev/docs/foundations/overview
 */

const { text } = await generateText({
  model: openai("gpt-4o-mini"),
  // model: anthropic("claude-3-5-sonnet-20241022"),
  // model: google("gemini-1.5-flash"),
  // model: xai("grok-beta"),
  prompt: "AI SDK에 대해 간단히 설명해주세요.",
})

console.log(text)
