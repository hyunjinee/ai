import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain import hub


def load_with_selenium(url):
    """Selenium을 사용하여 JavaScript가 렌더링된 페이지 콘텐츠를 가져옵니다."""
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Chrome 드라이버 시작
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # 페이지가 완전히 로드될 때까지 대기 (최대 10초)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # JavaScript 실행을 위한 추가 대기
        time.sleep(3)
        
        # 페이지 텍스트 추출
        page_text = driver.execute_script("return document.body.innerText")
        
        # Document 객체 생성
        doc = Document(page_content=page_text, metadata={"source": url})
        
        driver.quit()
        return [doc]
        
    except Exception as e:
        print(f"Selenium 로드 실패: {e}")
        if 'driver' in locals():
            driver.quit()
        return []


def main():
    parser = argparse.ArgumentParser(description='JavaScript 렌더링을 지원하는 RAG 시스템')
    parser.add_argument('--url', type=str, required=True, help='분석할 URL')
    parser.add_argument('--use-selenium', action='store_true', help='Selenium 사용 여부')
    
    args = parser.parse_args()
    url = args.url
    print(f"URL 분석 중: {url}")
    
    # 콘텐츠 로드
    if args.use_selenium:
        print("Selenium을 사용하여 JavaScript 렌더링 중...")
        data = load_with_selenium(url)
    else:
        from langchain_community.document_loaders import WebBaseLoader
        loader = WebBaseLoader(url)
        data = loader.load()
    
    if not data:
        print("콘텐츠를 로드할 수 없습니다.")
        return
    
    # 로드된 콘텐츠 확인
    print(f"\n=== 로드된 문서 내용 (처음 1000자) ===")
    print(data[0].page_content[:1000])
    print("="*50)
    
    # 텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(data)
    print(f"\n{len(all_splits)}개의 청크로 분할됨")
    
    # 벡터 저장소 생성
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=OllamaEmbeddings(model="nomic-embed-text")
    )
    
    # LLM 설정
    llm = OllamaLLM(
        model="llama3.2",
        verbose=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    
    # RAG 체인 설정
    QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )
    
    # 질문하기
    print("\n질문을 입력하세요 (종료: 'quit')")
    while True:
        question = input("\n질문: ")
        if question.lower() == 'quit':
            break
            
        result = qa_chain.invoke({"query": question})
        print(f"\n답변: {result['result']}")


if __name__ == "__main__":
    main()