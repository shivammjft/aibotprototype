import asyncio
from langchain_openai import OpenAIEmbeddings
import os
from datetime import datetime
from constants.email_constants import bot_ready_email_template
from utils.mailjet import send_email_with_template
from utils.text_processing_and_chunking import preprocess_text, chunk_text
from config.db import collection
from dotenv import load_dotenv
from utils.scraper_links import get_links
from utils.process_links import parallel_load
from qdrant_client import QdrantClient
from uuid import uuid4
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams


load_dotenv()

TOPIC_NAME = "COMPANY_INIT"

embeddings = OpenAIEmbeddings()

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
    client = QdrantClient(url="http://localhost:6333", timeout=60)
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
    
    print("----------------Storing in Pinecone Index----------------")
    vector_store.add_documents(documents=text_chunks, ids=uuids)

def callback(ch, method, properties, body):
    global bot_ready_email_template
    message = body.decode()
    print(f" [x] Received {message}")
    company_id = message
    company_document = collection.find_one({"company_id": company_id})
    if company_document:
        print(company_document)
        print("found ")
        collection_name = company_document['company_id'] 
        collection_metadata = company_document['metadata'] 
        email = collection_metadata["email"]
        print(collection_name, collection_metadata)
        
        # Run asynchronous process function
        asyncio.run(process(collection_metadata["base_link"], company_id))
        
        API_KEY = company_id
        email = collection_metadata["email"]
        company_name = collection_metadata["company_name"]
        base_link = collection_metadata["base_link"]
        chatbot_name = company_document["chatbot_name"]
        send_email_with_template(
        recipent_email=email,
        subject="Successfully Bot Created",
        company_id=company_id,
        company_name=company_name,
        base_link=base_link,
        API_KEY=API_KEY,
        chatbot_name=chatbot_name,
        template=bot_ready_email_template
    )
        print("ENDED ", datetime.now())
    else:
        print(f"Company with ID {company_id} not found in MongoDB.") 
