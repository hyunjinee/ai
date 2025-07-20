## 1. Ingest PDF Files
# 2. Extract Text from PDF Files and split into small chunks
# 3. Send the chunks to the embedding model
# 4. Save the embeddings to a vector database
# 5. Perform similarity search on the vector database to find similar documents
# 6. retrieve the similar documents and present them to the user
## run pip install -r requirements.txt to install the required packages

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader

import nltk

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('punkt_tab')
# nltk.download()
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('all') # 모든 패키지 다운로드 경우
# nltk.download('popular') #
# import nltk
# nltk.download('punkt_tab')

doc_path = "./data/BOI.pdf"
model = "llama3.2"

# Local PDF file uploads
if doc_path:
    print('start')
    loader = UnstructuredPDFLoader(file_path=doc_path)
    data = loader.load()
    print("done loading....")
else:
    print("Upload a PDF file")

    # Preview first page
content = data[0].page_content
print(content[:100])
