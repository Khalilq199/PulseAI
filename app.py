# in future add memory, maybe use conversation buffer memory

from flask import Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import * # import every public variable into app.py
import os

# initialized flask web app
app = Flask(__name__)


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = download_embeddings()

index_name = "pulseai"
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

chatmodel = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatmodel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)





#runs when a GET request is made tot he root URL
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"]) #macth the /get url, accept POST request and call chat()
def chat():
    msg = request.form["msg"] # read incoming data
    user_input = msg
    print(user_input)
    response = rag_chain.invoke({"input": msg}) #run AI pipeline
    print("Response : ", response["answer"])
    return str(response["answer"]) # return a response to the client with this content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug = True)
