import { createOllama } from "ollama-ai-provider-v2"
import {
  generateText,
  // LanguageModel,
  // LanguageModelV1,
  // LanguageModelV2,
} from "ai"

const ollama = createOllama({
  baseURL: "http://localhost:11434/api",
})
const a = ollama("llama3.2:1b")

const { text } = await generateText({
  // model: ollama("llama3.2:1b") as unknown as LanguageModel,
  model: ollama("qwen3:4b") as any,
  providerOptions: { ollama: { think: true } },
  prompt: "안녕 너는 누구야?",
})

console.log(text)
