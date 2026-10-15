import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llama_index.core import Settings, VEctorStoreIndex, StorageContext, Document
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms_ollama import ollama
from llama_index.vector_stores.postgres import PGVectorStore
import sqlalchemy
from dotenv import load_dotenv 

app. FastAPI(title="RRAG localcom FastAPI, LLamaIndex e Ollama")

load_dotenv(".env")

dbuser = os.getenv("DB_USER")
dbname = os.getenv("DB_NAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

dbconnection=f"postgresql://{dbuser}:{password}@{host}:{port}/{dbname}"

# Create a SQLAlchemy engine
engine = sqlalchemy.create_engine(dbconnection)

ollama_host = os.getenv("OLLAMA_HOST")
ollama_port = os.getenv("OLLAMA_PORT")
ollama_url = f"http://{ollama_host}:{ollama_port}"


# setting a ollama serve

Settings.llm = Ollama(model="llama3.1:8b", base_url=ollama_url, request_timeout=120.0 )
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url=ollama_url )

# initialize vector store of Postgres
def get_index():
    vector_store = PGVectorStore.from_params(
        database=dbname,
        host=dbhost,
        port=dbport,
        user=dbuser,
        password=password,
        table_name="vector_emberdings", 
        embed_dim=768, 
    )
    Storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, Storage_context=Storage_context)
    return index


class DocumentRequest(BaseModel):
    text:str

class QueryRequest(BaseModel):
    question: str


# FastAPI -

@post("/add_document")
def add_document(document_request:DocumentRequest):
    try:
        document = Document(text=document_request.text)
        # add the document to the vector store
        index = get_index()
        index.insert(document)
        return {"Status":"sucess"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@post("/query")
def query(query_request:QueryRequest):
    try:
        # query the vector store for relevant documents
        index = get_index()
        query_engine = index.as_query_engine()
        response = query_engine.query(query=query_request.question)
        return {
            "question":query.question,
            "response":str(response),
            "source_nodes":[node.text for node in response.source_nodes]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@get("/")
def health_check():
    return {"Status":"OK", "gpu_aceleration":"enabled via ollama"}

