import asyncio
from langchain_openai import OpenAIEmbeddings
import os
from datetime import datetime
import time
from constants.email_constants import bot_ready_email_template
from utils.mailjet import send_email_with_template
from utils.text_processing_and_chunking import preprocess_text, chunk_text
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from config.db import collection
from dotenv import load_dotenv
from utils.scraper_links import get_links
from utils.process_links import parallel_load


load_dotenv()

TOPIC_NAME = "COMPANY_INIT"

embeddings = OpenAIEmbeddings()

async def process(url, company_id):
    links = await get_links(url)
    print("----------------Crawling Data------------------------")
    docs = parallel_load(links, os.cpu_count())
    await prepare_DB(docs, company_id)

async def prepare_DB(docs, namespace_name):
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
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)

    embeddings = OpenAIEmbeddings()

    print("----------------Creating Index------------------------")
    index_name = "companyinit"

    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            ) 
        ) 
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    
    print("----------------Storing in Pinecone Index----------------")
    PineconeVectorStore.from_documents(
        text_chunks, embeddings, index_name=index_name, namespace=namespace_name
    )

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
