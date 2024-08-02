from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser
import uuid
from kafka import KafkaProducer
from typing import Optional
from fastapi import  HTTPException, Depends
from langchain_openai import OpenAIEmbeddings
import os
from typing import Optional
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from kafka import KafkaProducer
from utils.auth import get_current_user
from datetime import datetime
from models.schems import Company,ClientRequest
from config.db import collection
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOPIC_NAME = "COMPANY_INIT"


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Chatbot Doc Mapping"


producer = KafkaProducer(
    bootstrap_servers=f"kafka-33abc88c-jellyfishtechnologies-4169.b.aivencloud.com:27373",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

def on_send_success(record_metadata):
    print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} with offset {record_metadata.offset}")


def context_retriever(query, collection_name, namespace_name, embeddings=OpenAIEmbeddings()):
    try:
        vectorstore = PineconeVectorStore(index_name=collection_name, embedding=embeddings, namespace=namespace_name)
        docs = vectorstore.similarity_search(query, k=5)
        if len(docs) != 0:
            content = ""
            for i in range(len(docs)):
                try:
                    page_content = docs[i].page_content 
                    source = docs[i].metadata.get('source', "")
                    title = docs[i].metadata.get('title', "")
                    description = docs[i].metadata.get('description', "")
                    
                    content += f"""{i+1}. Content: {page_content}.\nContent's Page URL: {source}.\nTitle of the page: {title}.\nDescription of the page: {description}.\n"""
                except Exception as e:
                    content = f"An error occurred while processing document {i}: {str(e)}"
        else:
            content = "Frame a professional answer which shows the positive image of the company and should be relevant to the query"
            
    except Exception as e:
        content = f"An error occurred: {str(e)}"
    
    return content


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

embeddings = OpenAIEmbeddings()


class RequestModel(BaseModel):
    query: str
    context: Optional[list[str]] = None
    session_id: str


def generate_company_id() -> str:
    unique_id = uuid.uuid4()
    return str(unique_id)

user_message = """

<|Storyline|>
You are the {chatbot_name} an Assistant of the website: {base_url}. Your task is to answer queries of the chatbot user based on the most relevant context.\
Your primary goal is to guide users to contact the company through the contact details to discuss their needs and how company can help them.\
Each response should encourage the user to get in touch with the company.\
Your mission is to ensure every visitor is impressed with company and eager to take advantage of your services.\
Start by greeting the user warmly. Highlight the benefits of company's services and guide the user to the contact form to make a deal.\
Here are some key points to include in your responses:
- Highlight company's expertise if any.
- Emphasize the importance of getting a tailored solution from the sales team.
- With every response, always direct the user to the team with contact details. 

<|Instructions|>
You will be providing the answers to the queries, always give accurate answers which can impress the person visiting the website. Always give professional and formal answers.\
If any question is unprofessional or irrelevant to the benefits of the company like song, bomb threat, illegal activities, reply "Your question does not align with professional standards. If you have any inquiries related to company, please feel free to ask. I am happy to help."\
Make sure you always provide a positive image of company, do not provide unnecessary details.\
Do not give rough estimations/timeline of app development and projects. Direct them to the contact form.


<|Context|>
{context}\

<|Instructions|>
Use the above the context only to provide an answer in about 60 words kind of summary without missing any important information present in the context. Don't write according to the context. Stick to the role.\
If there is any URL related to the response of any query, provide relevant URLs with response.\
*If you don't know the answer, just say that you are still learning and improving yourself. Don't give anything on yourself*\
Strictly Answer in less than 60 words\
Strictly don't provide response in markdown\
"""



human_message_template = """
<|Question|>
{question}
"""



# creating prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", user_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# declaring llm
llm = ChatGroq(
    temperature=0.0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jellyfish Technologies AI!"}


# funtion for history retrieval using redis
def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=os.getenv("REDIS_URL"))


@app.post("/init_company/")
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
        docment = {
            "company_id": company_id,
            "metadata": data,
            "deployment_sources":req.deployment_link,
            "chatbot_name":req.chatbot_name,
            "model_build_status":True
        }
        collection.insert_one(docment)
        TOPIC_NAME ="COMPANY_INIT"
        producer.send(TOPIC_NAME, company_id.encode('utf-8'))
        producer.flush() 
        print(f"Message sent: {company_id}")
        return {"company": company_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/query")
async def answer_query(req: RequestModel,user: dict = Depends(get_current_user) ):
    try:
        collection_name = 'companyinit'
        namespace_name = user["company_id"]
        rag_chain = prompt | llm | StrOutputParser()
        with_message_history = RunnableWithMessageHistory(
            rag_chain,
            get_message_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        final_response = await with_message_history.ainvoke(
            {"context": context_retriever(req.query, collection_name, namespace_name), "input": req.query,"chatbot_name":user["chatbot_name"],"base_url":user["metadata"]["base_url"]},
            config={"configurable": {"session_id": req.session_id}},
        )
        return final_response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)