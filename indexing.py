# https://docs.kanaries.net/ko/topics/Streamlit/streamlit-chatbot
from langchain_community.document_loaders import DirectoryLoader

directory = "data/books"

def load_docs(directory):
 loader = DirectoryLoader(directory)
 documents = loader.load()
 return documents

documents = load_docs(directory)
print(len(documents))


# 문서를 로드한 후, 스크립트는 이러한 문서를 더 작은 청크로 분리합니다.
# 청크의 크기와 이러한 청크 사이의 오버랩은 사용자가 정의할 수 있습니다.
# 이렇게 함으로써 문서의 크기를 관리 가능한 수준으로 유지하고 분리로 인해 관련 정보가 누락되지 않도록합니다.
# 이를 위해 LangChain의 RecursiveCharacterTextSplitter 클래스가 사용됩니다.


from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_docs(documents,chunk_size=500,chunk_overlap=20):
 text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
 docs = text_splitter.split_documents(documents)
 return docs

docs = split_docs(documents)
print(docs)
print(len(docs))

# 문서가 분리되면 AI 모델이 이해할 수 있는 형식으로 이 텍스트 청크를 변환해야 합니다.
# 이는 LangChain에서 제공하는 SentenceTransformerEmbeddings 클래스를 사용하여 텍스트의 임베딩을 생성함으로써 수행됩니다.

from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 임베딩이 생성된 후, 쉽게 액세스하고 검색할 수 있는 곳에 저장되어야합니다.
# Pinecone은 이 작업에 적합한 벡터 데이터베이스 서비스입니다.
# 이 스크립트는 Pinecone에서 인덱스를 생성하고 임베딩을 해당 텍스트와 함께 저장합니다.
# 이제 사용자가 질문을 하면 chatbot은 이 인덱스에서 가장 유사한 텍스트를 검색하고 해당하는 답변을 반환할 수 있습니다.


