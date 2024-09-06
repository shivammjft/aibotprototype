from fastapi import Depends
import os
import datetime
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import RedisChatMessageHistory
import tiktoken
from models.tables import Queries
from config.db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("DEEP_INFRA_API_KEY"), model="meta-llama/Meta-Llama-3-70B-Instruct", base_url="https://api.deepinfra.com/v1/openai")

embeddings = OpenAIEmbeddings()


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

# funtion for history retrieval using redis
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=os.getenv("REDIS_URL"))


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)



def context_retriever(query,session_id,company_id,chatbot_id,db,collection_name, embeddings=OpenAIEmbeddings()):
    try:
        vectorstore = QdrantVectorStore.from_existing_collection(embedding=embeddings, collection_name=collection_name, url="qDrant_server:6333")
        docs = vectorstore.similarity_search(query, k=5)
        if len(docs) != 0:

            content = ""
            for i in range(len(docs)):
                try:
                    page_content = docs[i].page_content 
                    source = docs[i].metadata.get('source', "")
                    title = docs[i].metadata.get('title', "")
                    description = docs[i].metadata.get('description', "")
                    
                    content += f"""{i+1}. Content: {page_content}.\nContent's Page URL: {source}.\nTitle of the page: {title}.\nDescription of the page: {description}.\n"""
                except Exception as e:
                    content = f"An error occurred while processing document {i}: {str(e)}"
        else:
            content = "Frame a professional answer which shows the positive image of the company and should be relevant to the query, don't answer on your own if you think question is not relevant to companies benfits"
        
    except Exception as e:
        content = f"An error occurred: {str(e)}"
    create_query_model = Queries(
    company_id = company_id,
    chatbot_id = chatbot_id,
    session_id = session_id,
    query_text_user = query,
    query_context = content,
    query_time = datetime.datetime.now()
    )
    db.add(create_query_model)
    db.commit()
    return content


def count_tokens(text):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)

