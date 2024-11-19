import asyncio
from langchain_openai import OpenAIEmbeddings
import os
import json
from models.tables import Company, Chatbot_stats
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
from typing import Annotated
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams
from config.db import SessionLocal
import logging
import pymupdf4llm
from langchain_core.documents import Document

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOPIC_NAME = "COMPANY_INIT"

shared_folder_path = "/shareduploadfolder"

embeddings = OpenAIEmbeddings()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

async def process(url, company_id):
    links = await get_links(url)
    logger.info("----------------Crawling Data------------------------")
    docs = parallel_load(links, os.cpu_count())
    await prepare_DB(docs, company_id)

async def process_files(files, company_key):
    for file in files:
        temp_file_path = os.path.join(shared_folder_path, file.filename)
        logger.info(f"Processing file: {file.filename}")

        with open(temp_file_path, "rb") as temp_file:
            logger.info("Extracting markdown from the PDF")
            pdf_text = pymupdf4llm.to_markdown(temp_file)

            document = Document(
                page_content=pdf_text,
                metadata={"source": "Documents"}
            )
        logger.info("Chunking data for processing")
        text_chunks = chunk_text(document)

        logger.info(f"Total text chunks generated: {len(text_chunks)}")

        embeddings = OpenAIEmbeddings()
        client = QdrantClient(url="http://qdrant:6333", timeout=18000)
        logger.info("Client Initialized")

        collection_name = company_key
        logger.info(f"Collection Name: {collection_name}")
        logger.info(not client.collection_exists(collection_name))
        if not client.collection_exists(collection_name):
            logger.info(f"Collection '{collection_name}' does not exist. Creating it.")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        
        # Batch store chunks
        logger.info("Storing text chunks in Qdrant")
        batch_size = 100
        for i in range(0, len(text_chunks), batch_size):
            batch_chunks = text_chunks[i : i + batch_size]
            batch_uuids = [str(uuid4()) for _ in range(len(batch_chunks))]
            logger.info(f"Storing batch {i // batch_size + 1}/{(len(text_chunks) // batch_size) + 1}")
            retry_upsert(client, collection_name, batch_chunks, batch_uuids, embeddings)

        logger.info(f"File {file.filename} processed successfully.")

        os.remove(temp_file_path)



async def prepare_DB(docs, collection_name, batch_size=100, retry_attempts=3):
    logger.info("----------------Preparing Database--------------------")

    logger.info("----------------Preprocessing Data--------------------")
    for doc in docs:
        text = preprocess_text(doc.page_content)
        doc.page_content = text

    logger.info("-------------Chunking Data------------------------")
    text_chunks = chunk_text(docs)
    logger.info(f"Total number of text chunks: {len(text_chunks)}")

    logger.info("----------------Creating Embeddings--------------------")
    embeddings = OpenAIEmbeddings()

    logger.info("----------------Connecting to Qdrant-------------------")
    client = QdrantClient(url='http://qdrant:6333', timeout=18000) 

    if not client.collection_exists(collection_name):
        logger.info(f"Collection {collection_name} does not exist. Creating collection.")
        client.create_collection(
            collection_name=collection_name, 
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
    
    logger.info(f"Storing text chunks in batches of {batch_size}...")
    
    for i in range(0, len(text_chunks), batch_size):
        batch_chunks = text_chunks[i:i+batch_size]
        batch_uuids = [str(uuid4()) for _ in range(len(batch_chunks))]

        logger.info(f"Processing batch {i // batch_size + 1}: {len(batch_chunks)} chunks.")
        
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings,
        )
        
        await retry_upsert(vector_store, batch_chunks, batch_uuids, retry_attempts)
    
    logger.info(f"Successfully processed {len(text_chunks)} chunks.")


async def retry_upsert(vector_store, text_chunks, uuids, retries=3):
    for attempt in range(retries):
        try:
            logger.info(f"Attempt {attempt + 1} to store documents in Qdrant.")
            vector_store.add_documents(documents=text_chunks, ids=uuids)
            logger.info(f"Successfully stored {len(text_chunks)} documents in Qdrant.")
            break
        except Exception as e:
            logger.error(f"Error during upsert: {str(e)}")
            if attempt < retries - 1:
                logger.info(f"Retrying after attempt {attempt + 1}...")
                await asyncio.sleep(2 ** attempt)  
            else:
                logger.error(f"Failed to store documents in Qdrant after {retries} attempts.")
                raise e
            
async def callback(ch, method, properties, body):
    logger.info("Callback triggered")
    global bot_ready_email_template
    db = next(get_db())

    message = json.loads(body.decode())
    logger.info(f"Received message: {message}")
    company_key = message.get("company_key")
    chatbot_id = message.get("chatbot_id")
    upload_files= message.get("upload_files")
    company_document = db.query(Company).filter(Company.company_key == company_key).first()
    chatbot_document = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id == chatbot_id).first()


    if company_document:
        logger.info(f"Company document found: {company_document}")
        
        if len(upload_files)>0 :
            logger.info(f"Processing files for: {company_document.company_name}")
            processed_file_status = await process_files(upload_files, company_document.company_key)

        if company_document.base_url is not None:
            logger.info(f"Processing Site for: {company_document.company_name}")
            asyncio.run(process(company_document.base_url, company_key))

        email = company_document.email
        CHATBOT_KEY = chatbot_document.chatbot_id
        API_KEY = company_key
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
        
        logger.info("Done processing message")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Message acknowledged at {datetime.now()}")
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.warning(f"Company with ID {company_key} not found in the database.")
