from kafka import KafkaConsumer
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import requests
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time
from constants.email_constants import html_template
from utils.text_processing_and_chunking import preprocess_text, chunk_text
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from kafka import KafkaConsumer
from dotenv import load_dotenv
from utils.scraper_links import get_links
from utils.process_links import parallel_load
load_dotenv()


def send_email_smtp(subject, body, recipients):
    sender = os.getenv("SENDER")
    password = os.getenv("PASSWORD")
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")



# async def send_email(data):
#     url = 'https://formspree.io/f/xdkngzll' 

#     data= {"message":data} 

#     response = requests.post(url, data=data)

#     if response.status_code == 200:
#         print("Email sent successfully!")
#     else:
#         print(f"Failed to send email. Status code: {response.status_code}")
#         print(f"Response: {response.text}")


TOPIC_NAME = "COMPANY_INIT"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=f"kafka-33abc88c-jellyfishtechnologies-4169.b.aivencloud.com:27373",
    client_id = "CONSUMER_CLIENT_ID",
    group_id = "CONSUMER_GROUP_ID",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

embeddings = OpenAIEmbeddings()





async def prepare_DB(docs, collection_name, namespace_name):
    global TOPIC_NAME
    print("----------------Preparing Database--------------------")


    print("----------------Preprocessing Data--------------------")
    for doc in docs:
        text = preprocess_text(doc.page_content)
        doc.page_content = text
    
    print("----------------Chunking Data------------------------")
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



async def run(consumer,collection):
    while True:
        for message in consumer.poll().values():
            company_id=message[0].value.decode('utf-8')
            starttime= datetime.now()
            print("Started ::::",starttime)
            company_document = collection.find_one({"company_id": company_id})
            if company_document:
                print(company_document)
                print("found ")
                collection_name = company_document['company_id'] 
                collection_metadata = company_document['metadata'] 
                email=collection_metadata["email"]
                print(collection_name,collection_metadata)
                links =await get_links(collection_metadata["base_link"])
                print("----------------Crawling Data------------------------")
                docs =parallel_load(links,os.cpu_count())
                await prepare_DB(docs, collection_name, company_id)
                API_KEY = company_id
                email = collection_metadata["email"]
                company_name = collection_metadata["company_name"]
                base_link = collection_metadata["base_link"]
                chatbot_name = company_document["chatbot_name"]
                text = f"""
                 The AI model is trained. Now you can use the credentials to access your personal AI bot.
                

                
                Id: {company_id}
                Email: {email}
                Company Name: {company_name}
                Base Url: {base_link}
                

                Copy the code snippet below and insert it into your website's footer or header before the closing </body> tag without any modification.

                code_snippet:
                
                <script
                  id="ai-jellyfishbot"
                  src="https://aibotfiles.vercel.app/script.js"
                  defer >
                  {API_KEY},{company_name},{chatbot_name}
                </script>
                """
                send_email_smtp("Jellyfish AI Bot Notification",text,email)
                print("ENDED ",datetime.now())
            else:
                print(f"Company with ID {company_id} not found in MongoDB.") 




