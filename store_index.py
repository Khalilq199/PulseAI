"""
Currently this file collects all the pdf data from the data/ directory, extracts chunks and 
stores into the index, it rewirites. 

Future: add modules to add specific new files into the index for expanding knowledgebase, and 
woring with image embedding models aswell.
"""

from dotenv import load_dotenv
import os
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings

from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# loading keys into current python process
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

extracted_data = load_pdf_files("data")
minimal_docs = filter_to_minimal_docs(extracted_data)
texts_chunk = text_split(minimal_docs)

embedding = download_embeddings()

pinecone_api_key = PINECONE_API_KEY
# excecuting with pinecone account
pc = Pinecone(api_key=pinecone_api_key) #instance of the pinecone client

# creating vector database
index_name = "pulseai"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension=384, #dimension of the embeddings from the embedding model
        metric="cosine", #using cosine similarity for similarity search
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents=texts_chunk,
    embedding=embedding,
    index_name=index_name
)
