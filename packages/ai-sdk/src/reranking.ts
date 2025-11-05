import { rerank } from "ai"
import { cohere } from "@ai-sdk/cohere"

const documents = [
  "sunny day at the beach",
  "rainy afternoon in the city",
  "snowy night in the mountains",
]

const { ranking } = await rerank({
  model: cohere.reranking("rerank-v3.5"),
  documents,
  query: "talk about rain",
  topN: 2, // Return top 2 most relevant documents
})

console.log(ranking)
// [
//   { originalIndex: 1, score: 0.9, document: 'rainy afternoon in the city' },
//   { originalIndex: 0, score: 0.3, document: 'sunny day at the beach' }
// ]
