"""
This is a file containing resusable helper functions
"""

from langchain.document_loaders import PyPDFLoader, DirectoryLoader # loading pdf documents as Document objects
from langchain.text_splitter import RecursiveCharacterTextSplitter # intelligently splits text
from langchain.schema import Document # import langchain document object
from langchain_huggingface import HuggingFaceEmbeddings

from typing import List


# Extract text from pdf files
def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    return documents

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """

    # go through all the documents created of pdfs, filter out all metadata but source
    minimal_docs : List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

# split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        # 500 tokens (characters) as one chunk
        chunk_size=500,
        #need chunk overlap for model context, each chunk shares 20 characters with the next chunk
        chunk_overlap=20,
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk

def download_embeddings():
    # Download and return the HuggingFace embeddings model.

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings

embedding = download_embeddings()
