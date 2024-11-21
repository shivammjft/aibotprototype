from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import Annotated, Dict, List
from routers.auth import get_current_user_with_token
from models.tables import Chatbot_stats, Company, Queries, QueryUsers,Users
from models.schemas import QueryUserResponse
import os
import logging
import pymupdf4llm
from models.schemas import UpdatePromptRequest
from sqlalchemy.exc import NoResultFound
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from uuid import uuid4
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from langchain_core.documents import Document


router = APIRouter(prefix='/admin', tags=['Admin'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_TOKEN_RATE = 0.35 / 1_000_000
OUTPUT_TOKEN_RATE = 0.40 / 1_000_000

def company_to_dict(company, total_queries) -> Dict:
    input_token_cost = float(company.input_tokens * INPUT_TOKEN_RATE)  
    output_token_cost = float(company.output_tokens * OUTPUT_TOKEN_RATE) 

    return {
        "id": company.id,
        "company_key": company.company_key,
        "input_tokens": company.input_tokens,
        "created_date": company.created_date.isoformat(),
        "company_name": company.company_name,
        "base_url": company.base_url,
        "email": company.email,
        "output_tokens": company.output_tokens,
        "input_token_cost": input_token_cost,
        "output_token_cost": output_token_cost,
        "total_queries": float(total_queries) 
    }

def chunk_text(text, chunk_size=600, chunk_overlap=60):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents([text])
    return chunks

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user_with_token)]

@router.get("/total-stats")
async def get_total_stats(db: db_dependency, user: user_dependency):
    try:
        total_input_tokens = db.query(func.sum(Company.input_tokens)).scalar() or 0
        total_output_tokens = db.query(func.sum(Company.output_tokens)).scalar() or 0
        total_queries = db.query(func.count(Queries.id)).scalar() or 0
        
        total_input_tokens = Decimal(total_input_tokens)
        total_output_tokens = Decimal(total_output_tokens)

        dollar_spend_input = total_input_tokens * Decimal(INPUT_TOKEN_RATE)
        dollar_spend_output = total_output_tokens * Decimal(OUTPUT_TOKEN_RATE)
        total_dollar_spend = dollar_spend_input + dollar_spend_output

        logger.info("Total stats retrieved successfully.")
        
        return JSONResponse(content={
            "status": "200",
            "data": {
                "input_tokens": float(total_input_tokens),
                "output_tokens": float(total_output_tokens),
                "requests": total_queries,
                "dollar_spend_input": float(dollar_spend_input),
                "dollar_spend_output": float(dollar_spend_output),
                "dollar_spend_total": float(total_dollar_spend)
            }
        })
    except Exception as e:
        logger.error("Error retrieving total stats: %s", str(e))
        raise HTTPException(status_code=500, detail="Something went wrong; not able to get the total stats")

@router.get("/companies", status_code=status.HTTP_200_OK)
async def all_companies(db: db_dependency, user: user_dependency):
    try:
        companies = db.query(Company).all()
        total_queries_by_company = (
            db.query(Chatbot_stats.company_id, func.sum(Chatbot_stats.total_queries).label("total_queries"))
            .group_by(Chatbot_stats.company_id)
            .all()
        )

        total_queries_dict = {company_id: total_queries for company_id, total_queries in total_queries_by_company}
        companies_list = [
            company_to_dict(company, total_queries_dict.get(company.id, 0)) for company in companies
        ]
        logger.info("Fetched %d companies.", len(companies_list))
        
        return JSONResponse(content={
            "status": status.HTTP_200_OK,
            "data": companies_list
        })
    except Exception as e:
        logger.error("Error fetching companies: %s", str(e))
        raise HTTPException(status_code=500, detail="Unable to fetch all companies")

@router.get("/companies/{company_id}/chatbots", status_code=status.HTTP_200_OK)
async def get_chatbots(company_id: int, db: db_dependency, user: user_dependency):
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            logger.warning("Company not found: %d", company_id)
            raise HTTPException(status_code=404, detail="Company not found")

        chatbots = db.query(Chatbot_stats).filter(Chatbot_stats.company_id == company_id).all()
        chatbots_list = []

        for chatbot in chatbots:
            input_token_cost = Decimal(chatbot.total_input_tokens) * Decimal(INPUT_TOKEN_RATE)
            output_token_cost = Decimal(chatbot.total_output_tokens) * Decimal(OUTPUT_TOKEN_RATE)

            chatbot_info = {
                "chatbot_id": chatbot.chatbot_id,
                "chatbot_name": chatbot.chatbot_name,
                "origin_url": chatbot.origin_url,
                "total_input_tokens": chatbot.total_input_tokens,
                "total_output_tokens": chatbot.total_output_tokens,
                "total_queries": chatbot.total_queries,
                "last_query_time": chatbot.last_query_time.isoformat() if chatbot.last_query_time else None,
                "input_token_cost": float(input_token_cost),
                "output_token_cost": float(output_token_cost),
                "total_token_cost": float(input_token_cost + output_token_cost)
            }

            chatbots_list.append(chatbot_info)

        logger.info("Fetched %d chatbots for company ID: %d", len(chatbots_list), company_id)
        
        return JSONResponse(content={
            "status": status.HTTP_200_OK,
            "data": chatbots_list
        })
    except Exception as e:
        logger.error("Error fetching chatbots: %s", str(e))
        raise HTTPException(status_code=500, detail="Unable to fetch chatbots")

@router.get("/chatbots/{chatbot_id}/queries", status_code=status.HTTP_200_OK)
async def get_queries_by_chatbot(chatbot_id: str, db: db_dependency, user: user_dependency):
    try:
        queries = db.query(Queries).filter(Queries.chatbot_id == chatbot_id).all()
        
        if not queries:
            logger.warning("No queries found for chatbot ID: %s", chatbot_id)
            raise HTTPException(status_code=404, detail="No queries found for this chatbot")

        queries_list = []
        for query in queries:
            queries_info = {
                "id": query.id,
                "session_id": query.session_id,
                "query_text_bot": query.query_text_bot,
                "query_text_user": query.query_text_user,
                "query_context": query.query_context,
                "input_tokens": query.input_tokens,
                "output_tokens": query.output_tokens,
                "query_time": query.query_time.isoformat() if query.query_time else None,
                "origin_url": query.origin_url
            }

            queries_list.append(queries_info)

        logger.info("Fetched %d queries for chatbot ID: %s", len(queries_list), chatbot_id)
        
        return JSONResponse(content={
            "status": status.HTTP_200_OK,
            "data": queries_list
        })
    except Exception as e:
        logger.error("Error fetching queries: %s", str(e))
        raise HTTPException(status_code=500, detail="Unable to fetch queries")
    


@router.post("/upload/")
async def upload_and_process_files(user: user_dependency, db:db_dependency, files: List[UploadFile] = File(...)):
    print(user)
    userdb = db.query(Users).filter(Users.username == user["username"]).first()
    company = db.query(Company).filter(Company.email == userdb.email).first()

    print(user.get("email"))
    folder_name = f"{company.company_name}-{company.company_key}"
    dir_path = os.path.join("uploads", folder_name)
    os.makedirs(dir_path, exist_ok=True)

    processed_files = []
    try:
        for file in files:
            temp_file_path = os.path.join(dir_path, file.filename)

            with open(temp_file_path, "wb") as buffer:
                buffer.write(await file.read()) 

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
            client = QdrantClient(url="http://localhost:6333", timeout=18000)
            logger.info("Client Initialized")

            collection_name = company.company_key
            logger.info(f"Collection Name: {collection_name}")
            if not client.collection_exists(collection_name):
                print("hi")
                logger.info(f"Collection '{collection_name}' does not exist. Creating it.")
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
            print("Hi")

            # Batch store chunks
            logger.info("Storing text chunks in Qdrant")
            batch_size = 100
            for i in range(0, len(text_chunks), batch_size):
                batch_chunks = text_chunks[i : i + batch_size]
                batch_uuids = [str(uuid4()) for _ in range(len(batch_chunks))]
                logger.info(f"Storing batch {i // batch_size + 1}/{(len(text_chunks) // batch_size) + 1}")
                retry_upsert(client, collection_name, batch_chunks, batch_uuids, embeddings)

            logger.info(f"File {file.filename} processed successfully.")
            processed_files.append(file.filename)

            os.remove(temp_file_path)

        if not os.listdir(dir_path):
            os.rmdir(dir_path)

        return {"processed_files": processed_files} 

    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing files")

    finally:
        if os.path.exists(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)

            
@router.put("/chatbot/{chatbot_id}/prompt")
async def update_chatbot_prompt(chatbot_id: str, prompt_request: UpdatePromptRequest, user: user_dependency, db: Session = Depends(get_db)):
    try:
        chatbot = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id == chatbot_id).first()
        if chatbot is None:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        chatbot.chatbot_prompt = prompt_request.chatbot_prompt
        db.commit()
        db.refresh(chatbot)
        
        return {"message": "Chatbot prompt updated successfully", "chatbot_id": chatbot.chatbot_id, "chatbot_prompt": chatbot.chatbot_prompt}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    


@router.get("/chatbots/{chatbot_id}/query-users", response_model=List[QueryUserResponse], status_code=status.HTTP_200_OK)
async def get_users_by_chatbot(chatbot_id: str, db: Session = Depends(get_db)):
    try:
        query_users = db.query(QueryUsers).filter(QueryUsers.chatbot_id == chatbot_id).all()

        if not query_users:
            logger.warning("No users found for chatbot ID: %s", chatbot_id)
            raise HTTPException(status_code=404, detail="No users found for this chatbot")

        users_list = []
        for query_user in query_users:
            user_info = {
                "id": query_user.id,
                "session_id": query_user.session_id,
                "ip_address": query_user.ip_address,
                "origin_url": query_user.origin_url,
                "timezone":query_user.timezone,
            "language":query_user.language,
            "is_mobile":query_user.is_mobile,
            "user_agent":query_user.user_agent,
            "platform":query_user.platform,
            "referrer":query_user.referrer,
            "location":query_user.location,
            "network_type":query_user.network_type
            }
            users_list.append(user_info)

        logger.info("Fetched %d users for chatbot ID: %s", len(users_list), chatbot_id)
        
        return users_list
    except Exception as e:
        logger.error("Error fetching users: %s", str(e))
        raise HTTPException(status_code=500, detail="Unable to fetch users")