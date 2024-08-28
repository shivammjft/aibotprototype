from fastapi import APIRouter,Depends, HTTPException
from models.schems import ClientRequest
from utils.prepare_bot_utils import generate_company_id
from typing import Annotated
from datetime import datetime
import pika
from models.tables import Company
from config.db import SesssionLocal
from sqlalchemy.orm import Session




router = APIRouter(
    tags=['prepare']
)


def get_db():
    db = SesssionLocal()
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
        company_id = generate_company_id()
        create_company_model = Company(
        company_key = company_id,
        base_url= req.base_url,
        email = req.email,
        company_name = req.company_name,
        created_date = datetime.now()
        )
        db.add(create_company_model)
        db.commit()
        # QUEUE_NAME ="COMPANY_INIT"
        # connection = pika.BlockingConnection(
        # pika.ConnectionParameters(host='localhost'))
        # channel = connection.channel()
        # channel.queue_declare(queue=QUEUE_NAME, durable=True)
        # channel.basic_publish(
        #     exchange='',
        #     routing_key=QUEUE_NAME,
        #     body=company_id,
        #     properties=pika.BasicProperties(
        #         delivery_mode=pika.DeliveryMode.Persistent
        #     )
        # )
        # connection.close()
        print(f"Message sent: {company_id}")
        return {"company": company_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))