from fastapi import APIRouter,Depends, HTTPException
from models.schems import ClientRequest
from utils.prepare_bot_utils import generate_company_id
from config.db import collection
from datetime import datetime
import pika


router = APIRouter(
    tags=['prepare']
)


@router.post("/init_company/")
def add_company(req: ClientRequest):
    try:
        print(req)
        existing_company = collection.find_one({"email": req.email})
        if existing_company and existing_company["model_status"]:
            return {"detail": "Company with this email already exists and the Model training is in progress."}
        if existing_company and not existing_company["model_status"]:
            return {"detail": "Company with this email already exists and the Model training is done please check your email for credentials and code snippet."}
        company_id = generate_company_id()
        data={
        "company_name":req.company_name,
        "email":req.email,
        "base_link":req.base_link,
        "created_at":datetime.now(),
        "updated_at":datetime.now(),
        "links":None
        }
        document = {
            "company_id": company_id,
            "metadata": data,
            "deployment_sources":req.deployment_link,
            "chatbot_name":req.chatbot_name,
            "model_build_status":True
        }
        print(document)
        collection.insert_one(document)
        QUEUE_NAME ="COMPANY_INIT"
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=company_id,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        connection.close()
        print(f"Message sent: {company_id}")
        return {"company": company_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))