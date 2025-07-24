# RAG From Scratch

https://github.com/langchain-ai/rag-from-scratch

대규모 언어 모델(LLM)은 방대한 고정된 데이터 코퍼스에 기반하여 학습되었기 때문에, 비공개 정보나 최신 정보에 대한 추론 능력이 제한적입니다. 이를 해결하기 위한 방법 중 하나로 파인튜닝(fine-tuning)이 있지만, 이는 [사실적 회상(factual recall)에 적합하지 않은 경우가 많고](https://www.anyscale.com/blog/fine-tuning-is-for-form-not-facts), [비용이 많이 들 수 있습니다.](https://www.glean.com/blog/how-to-build-an-ai-assistant-for-the-enterprise)

RAG(Retrieval-Augmented Generation)는 LLM의 지식 기반을 확장하기 위한 강력하고 인기 있는 메커니즘으로 떠오르고 있습니다. 이 방법은 외부 데이터 소스에서 문서를 검색하여, 이를 기반으로 LLM이 컨텍스트 학습(in-context learning)을 통해 생성 작업을 수행하도록 합니다.

이 노트북 시리즈는 [동영상 재생목록](https://youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&feature=shared)을 보조하며, RAG에 대한 기초 개념부터 인덱싱(indexing), 검색(retrieval), 그리고 생성(generation)까지의 과정을 단계적으로 이해할 수 있도록 구성되어 있습니다.

![rag_detail_v2](https://github.com/langchain-ai/rag-from-scratch/assets/122662504/54a2d76c-b07e-49e7-b4ce-fc45667360a1)
