import "dotenv/config"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

/**
 * AI SDK 기본 예시
 *
 * 이 파일은 AI SDK의 기본적인 사용법을 보여줍니다.
 */

async function main() {
  console.log("🚀 AI SDK 예시 시작\n")

  try {
    // OpenAI를 사용한 텍스트 생성
    const { text } = await generateText({
      model: openai("gpt-4o-mini"),
      prompt: "AI SDK에 대해 간단히 설명해주세요.",
    })

    console.log("📝 생성된 텍스트:\n")
    console.log(text)
    console.log("\n✅ 완료!")
  } catch (error) {
    console.error("❌ 에러 발생:", error)

    if (error instanceof Error) {
      if (error.message.includes("API key")) {
        console.log("\n💡 .env 파일에 OPENAI_API_KEY를 설정해주세요.")
      }
    }
  }
}

main()
