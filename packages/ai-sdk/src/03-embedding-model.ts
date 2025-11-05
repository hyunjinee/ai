/**
 * **임베딩 모델(Embedding Models)**은 단어나 이미지 같은 복잡한 데이터를 ‘임베딩(embedding)’이라 불리는 벡터(숫자 리스트) 형태로 변환하는데 사용됩니다.
 * 생성형 모델과 달리, 임베딩 모델은 새로운 텍스트나 데이터를 생성하지 않습니다.
 * 대신, 개체 간의 의미적·구문적 관계를 수치적으로 표현하여 다른 모델이나 자연어 처리 작업의 입력으로 활용할 수 있게 합니다.
 */

import { ollama } from "ollama-ai-provider-v2"
import { cosineSimilarity, embedMany } from "ai"

const model = ollama.textEmbeddingModel("nomic-embed-text")

const { embeddings } = await embedMany({
  model: model as any,
  values: ["sunny day at the beach", "rainy afternoon in the city"],
})

console.log(
  `cosine similarity: ${cosineSimilarity(embeddings[0], embeddings[1])}`
)
