from fastapi import FastAPI
from consumer import callback
import pika
import threading
from dotenv import load_dotenv
import logging
import os
load_dotenv()
app = FastAPI()

QUEUE_NAME = "COMPANY_INIT"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_rabbitmq_consumer():
    try:
        logger.info('Starting RabbitMQ consumer...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        logger.info('Waiting for messages...')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")

@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

@app.get("/health")
def read_root():
    return {"message": "Server is up and running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
