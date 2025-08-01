import argparse
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM 
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain import hub

def main():
    parser = argparse.ArgumentParser(description='Filter out URL argument.')
    parser.add_argument('--url', type=str, default='http://example.com', required=True, help='The URL to filter out.')

    args = parser.parse_args()
    url = args.url
    print(f"using URL: {url}")

    loader = WebBaseLoader(url)
    data = loader.load()

    # Debug: 실제 로드된 콘텐츠 확인
    # print(f"\n=== 로드된 문서 내용 (처음 500자) ===")
    # if data:
    #     print(data[0].page_content[:500])
    # print("="*50)

    # Split into chunks 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    all_splits = text_splitter.split_documents(data)
    print(f"Split into {len(all_splits)} chunks")

    vectorstore = Chroma.from_documents(documents=all_splits,
                                        embedding=OllamaEmbeddings(model="nomic-embed-text"))

    # Debug: 질문에 대한 검색 결과 확인
    question = f"What are the latest headlines on {url}?"
    docs = vectorstore.similarity_search(question, k=3)
    print(f"\n=== 검색된 문서 (상위 3개) ===")
    for i, doc in enumerate(docs):
        print(f"\n문서 {i+1}:")
        print(doc.page_content[:300])
    print("="*50)

    print(f"Loaded {len(data)} documents")
    # print(f"Retrieved {len(docs)} documents")

   
    QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")

    # LLM
    llm = OllamaLLM(model="llama3.2",
                    verbose=True,
                    callbacks=[StreamingStdOutCallbackHandler()])
    print(f"Loaded LLM model {llm.model}")




    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},

    )

    # Ask a question
    question = "What is this page about? Summarize the main content."
    result = qa_chain.invoke({"query": question})

    print(result)
    


if __name__ == "__main__":
    main()