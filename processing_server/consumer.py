import asyncio
from langchain_openai import OpenAIEmbeddings
import os
import json
from models.tables import Company,Chatbot_stats
from fastapi import Depends
from datetime import datetime
from constants.email_constants import bot_ready_email_template
from utils.mailjet import send_email_with_template
from utils.text_processing_and_chunking import preprocess_text, chunk_text
from dotenv import load_dotenv
from utils.scraper_links import get_links
from utils.process_links import parallel_load
from qdrant_client import QdrantClient
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Annotated
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams
from config.db import SessionLocal
from sqlalchemy.orm import Session

load_dotenv()

TOPIC_NAME = "COMPANY_INIT"

embeddings = OpenAIEmbeddings()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


async def process(url, company_id):
    links = await get_links(url)
    print("----------------Crawling Data------------------------")
    docs = parallel_load(links, os.cpu_count())
    await prepare_DB(docs, company_id)

async def prepare_DB(docs, collection_name):
    global TOPIC_NAME
    print("----------------Preparing Database--------------------")

    print("----------------Preprocessing Data--------------------")
    for doc in docs:
        text = preprocess_text(doc.page_content)
        doc.page_content = text
    
    print("-------------import requests---Chunking Data------------------------")
    text_chunks = chunk_text(docs)
    print(len(text_chunks))

    print("----------------Creating Embeddings--------------------")
    embeddings = OpenAIEmbeddings()

    print("----------------Creating Index------------------------")

    uuids = [str(uuid4()) for _ in range(len(text_chunks))]
    client = QdrantClient(url="qDrant_server:6333", timeout=60)
    print("Hi")
    if not client.collection_exists(collection_name):
        #print("Hi1")
        client.create_collection(collection_name=collection_name,vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
        #print("Hi2")
    print("----------------Storing in Qdrant Collection----------------")
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )
    
    print("----------------Storing in Qdrant Index----------------")
    vector_store.add_documents(documents=text_chunks, ids=uuids)


def callback(ch, method, properties, body):
    global bot_ready_email_template
    db = next(get_db())

    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    company_key = message.get("company_key")
    chatbot_id = message.get("chatbot_id")
    company_document = db.query(Company).filter(Company.company_key == company_key).first()
    chatbot_document = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id ==chatbot_id).first()
    if company_document:
        print(company_document)
        print("found ")
        collection_name = company_document.company_key
        email = company_document.email
        
        # Run asynchronous process function
        asyncio.run(process(company_document.base_url,company_key))
        CHATBOT_KEY = chatbot_document.chatbot_id
        API_KEY = company_key
        email = company_document.email
        company_name = company_document.company_name
        base_link = company_document.base_url
        send_email_with_template(
        recipent_email=email,
        subject="Successfully Bot Created",
        company_id=company_key,
        company_name=company_name,
        base_link=base_link,
        API_KEY=API_KEY,
        CHATBOT_KEY=CHATBOT_KEY,
        chatbot_name=chatbot_document.chatbot_name,
        template=bot_ready_email_template
    )
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("ENDED ", datetime.now())
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Company with ID {company_key} not found in Db.") 
