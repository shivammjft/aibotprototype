from fastapi import APIRouter, Depends, HTTPException
from models.schemas import ClientRequest
from utils.prepare_bot_utils import generate_unique_id
from typing import Annotated
from datetime import datetime
from models.tables import Company, Chatbot_stats
from config.db import SessionLocal
from sqlalchemy.orm import Session
import pika
import json
import logging
import os
from dotenv import load_dotenv
from constants.prompts import user_message
from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import Annotated, Dict, List
from routers.auth import get_current_user, get_current_user_with_token
from models.tables import Chatbot_stats, Company, Queries, QueryUsers,Users
from models.schemas import QueryUserResponse
from pydantic import HttpUrl, BaseModel, Field, EmailStr
import os
import logging
import pymupdf4llm
import pathlib
from models.schemas import UpdatePromptRequest
from sqlalchemy.exc import NoResultFound
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from uuid import uuid4
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from langchain_core.documents import Document
from typing import Optional, List, Dict, Any


load_dotenv()

router = APIRouter(tags=['prepare'])

shared_folder_path = "/shareduploadfolder"

def chunk_text(text, chunk_size=600, chunk_overlap=60):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents([text])
    return chunks


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def retry_upsert(client, collection_name, text_chunks, uuids, embeddings, retries=3):
    
    for attempt in range(retries):
        try:
            logger.info(f"Upsert attempt {attempt + 1}")
            vector_store = QdrantVectorStore(
                client=client,
                collection_name=collection_name,
                embedding=embeddings,
            )
            vector_store.add_documents(documents=text_chunks, ids=uuids)
            logger.info(f"Successfully upserted {len(text_chunks)} documents.")
            break
        except Exception as e:
            logger.error(f"Error during upsert attempt {attempt + 1}: {str(e)}")
            if attempt < retries - 1:
                logger.info(f"Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
            else:
                logger.error("Max retries reached. Failing the upsert operation.")
                raise

def validate_base_url_or_files(
    base_url: Optional[HttpUrl] = None,
    files: Optional[List[UploadFile]] = None
):
    """
    Validation function to ensure at least one of base_url or files is provided.
    """
    if not base_url and not files:
        raise HTTPException(
            status_code=400,
            detail="Either 'base_url' or 'files' must be provided."
        )
    


@router.post("/init_company/")
async def add_company(db: db_dependency, 
                company_name : str = Form(...),
                chatbot_name: str =  Form(...),
                email:str = Form(...),
                deployment_url:Optional[HttpUrl] = Form(...),
                base_url : Optional[HttpUrl] = Form(None),
                files: List[UploadFile] = File(None)):
    try:
        if not base_url and not files:
            return JSONResponse(status_code=200, content={'detail': "Either provide base_url or files for creation"})
        
        logger.info("Received request to add company: %s")

        company = db.query(Company).filter(Company.email == email).first()
        if company:
            logger.warning("Company with this email already exists: %s", email)
            return {"detail": "Company with this email already exists."}

        company_key_id = generate_unique_id()
        create_company_model = Company(
            company_key=company_key_id,
            base_url=base_url,
            email=email,
            input_tokens=0,
            output_tokens=0,
            company_name=company_name,
            created_date=datetime.now()
        )

        db.add(create_company_model)
        db.commit()
        
        company_id = create_company_model.id

        chatbot_id = generate_unique_id()
        create_chatbot_model = Chatbot_stats(
            chatbot_id=chatbot_id,
            chatbot_name=chatbot_name,
            chatbot_prompt=user_message,
            company_id=company_id,
            origin_url=deployment_url,
            company_name=company_name,
            total_input_tokens=0,
            total_output_tokens=0,
            total_queries=0,
            last_query_time=datetime.now(),
        )
    
        db.add(create_chatbot_model)

        if files: 
            uploaded_files = []
            for file in files:
                file_path = os.path.join(shared_folder_path, file.filename)
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                uploaded_files.append(file.filename)  

        message_body = {
            "company_key": company_key_id,
            "chatbot_id": chatbot_id,
            "upload_files":uploaded_files
        }
        message_body_json = json.dumps(message_body)
        QUEUE_NAME = "COMPANY_INIT"

        logger.info("Connecting to RabbitMQ to send message.")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message_body_json,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        connection.close()
        
        logger.info("Message sent to RabbitMQ: %s", message_body_json)
        db.commit()
        return {"company": company_key_id}

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))




