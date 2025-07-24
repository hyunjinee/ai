from langchain.document_loaders import DirectoryLoader

DATA_PATH = "data/books"

def load_documents(data_path):
    loader = DirectoryLoader(data_path, glob="*.md")
    documents = loader.load()
    return documents
