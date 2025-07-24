import logging
import os

import ollama
import streamlit as st
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)

DOC_DIR = "./data/musicfe/"
MODEL_NAME = "gemma:7b"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_STORE_NAME = "simple-rag"
PERSIST_DIRECTORY = "./chroma_db"


def get_pdf_files(directory):
    """디렉토리에서 모든 PDF 파일 목록을 가져옵니다."""
    pdf_files = []
    for file in os.listdir(directory):
        if file.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files


def ingest_pdfs(pdf_files):
    """여러 PDF 문서를 로드합니다."""
    all_documents = []
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            loader = UnstructuredPDFLoader(file_path=pdf_file)
            data = loader.load()
            all_documents.extend(data)
            logging.info(f"PDF loaded successfully: {pdf_file}")
        else:
            logging.error(f"PDF file not found at path: {pdf_file}")

    if not all_documents:
        st.error("No PDF files were loaded successfully.")
        return None

    return all_documents


def ingest_pdf(doc_path):
    """Load PDF documents."""
    if os.path.exists(doc_path):
        loader = UnstructuredPDFLoader(file_path=doc_path)
        data = loader.load()
        logging.info("PDF loaded successfully.")
        return data
    else:
        logging.error(f"PDF file not found at path: {doc_path}")
        st.error("PDF file not found.")
        return None


def split_documents(documents):
    """Split documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(documents)
    logging.info("Documents split into chunks.")
    return chunks


@st.cache_resource
def load_vector_db():
    """벡터 데이터베이스를 로드하거나 생성합니다."""
    ollama.pull(EMBEDDING_MODEL)
    embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

    if os.path.exists(PERSIST_DIRECTORY):
        vector_db = Chroma(
            embedding_function=embedding,
            collection_name=VECTOR_STORE_NAME,
            persist_directory=PERSIST_DIRECTORY,
        )
        logging.info("Loaded existing vector database.")
    else:
        pdf_files = get_pdf_files(DOC_DIR)
        if not pdf_files:
            st.error("No PDF files found in the directory.")
            return None

        data = ingest_pdfs(pdf_files)
        if data is None:
            return None

        # 문서를 청크로 분할
        chunks = split_documents(data)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name=VECTOR_STORE_NAME,
            persist_directory=PERSIST_DIRECTORY,
        )
        vector_db.persist()
        logging.info("Vector database created and persisted.")
    return vector_db


def create_retriever(vector_db, llm):
    """Create a multi-query retriever."""
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""너의 이름은 뮤직이야.
        너의 임무는 주어진 사용자 질문의 5가지 다른 버전을 생성하여 벡터 데이터베이스에서 관련 문서를 검색하는 것이다.
        사용자 질문에 대해서 여러 관점을 생성하여 너의 목표는 사용자가 거리 기반 유사성 검색의 일부 제한을 극복하도록 돕는 것이다.
        줄 바꿈으로 구분된 대체 질문을 제공.
        원래 질문: {question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
    )
    logging.info("Retriever created.")
    return retriever


def create_chain(retriever, llm):
    """Create the chain with preserved syntax."""
    # RAG prompt
    template = """다음 문맥을 기반으로 질문에 답변하세요:
        {context}
        질문: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logging.info("Chain created with preserved syntax.")
    return chain


def main():
    st.title("뮤직이")

    # User input
    user_input = st.text_input("Enter your question:", "")

    if user_input:
        with st.spinner("Generating response..."):
            try:
                llm = ChatOllama(model=MODEL_NAME)

                # Load the vector database
                vector_db = load_vector_db()
                if vector_db is None:
                    st.error("Failed to load or create the vector database.")
                    return

                # Create the retriever
                retriever = create_retriever(vector_db, llm)

                # Create the chain
                chain = create_chain(retriever, llm)

                # Get the response
                response = chain.invoke(input=user_input)

                st.markdown("**Assistant:**")
                # st.write(response)
                response_container = st.empty()
                full_response = ""

                # 스트리밍 응답 처리
                for chunk in chain.stream(input=user_input):
                    if isinstance(chunk, str):
                        full_response += chunk
                    else:
                        full_response += chunk.content
                    # 실시간으로 응답 업데이트
                    response_container.markdown(full_response + "▌")

                # 최종 응답 표시
                response_container.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please enter a question to get started.")


if __name__ == "__main__":
    main()
