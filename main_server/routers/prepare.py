from fastapi import APIRouter,Depends, HTTPException
from models.schems import ClientRequest
from utils.prepare_bot_utils import generate_unique_id
from typing import Annotated
from datetime import datetime
from models.tables import Company,Chatbot_stats
from config.db import SessionLocal
from sqlalchemy.orm import Session
import pika
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    tags=['prepare']
)


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/init_company/")
def add_company(req: ClientRequest, db:db_dependency):
    try:
        print(req)
        company = db.query(Company).filter(Company.email == req.email).first()
        if company :
            return {"detail": "Company with this email already exists."}
        # if existing_company and not existing_company["model_status"]:
        #     return {"detail": "Company with this email already exists and the Model training is done please check your email for credentials and code snippet."}
        company_key_id = generate_unique_id()
        create_company_model = Company(
        company_key = company_key_id,
        base_url= req.base_url,
        email = req.email,
        input_tokens =0,
        output_tokens =0,
        company_name = req.company_name,
        created_date = datetime.now()
        )

        db.add(create_company_model)
        db.commit()
        
        company_id = create_company_model.id

        chatbot_id = generate_unique_id()
        create_chatbot_model = Chatbot_stats(
        chatbot_id = chatbot_id,
        chatbot_name  = req.chatbot_name,
        company_id = company_id,
        origin_url = req.deployment_url,
        company_name = req.company_name,
        total_input_tokens = 0,
        total_output_tokens= 0,
        total_queries =0,
        last_query_time = datetime.now(),
        )
        db.add(create_chatbot_model)
        message_body = {
            "company_key":company_key_id,
            "chatbot_id":chatbot_id
        }
        message_body_json = json.dumps(message_body)
        QUEUE_NAME ="COMPANY_INIT"
        print("sgasd")
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq_server'))
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
        print(f"Message sent: {company_key_id}")
        db.commit()
        return {"company": company_key_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

