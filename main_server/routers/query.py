from fastapi import APIRouter,Depends,HTTPException, Request
from utils.auth import get_current_user
from utils.query_utils import llm,get_message_history,context_retriever
from constants.prompts import user_message,human_message_template
from models.schems import RequestModel 
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from models.tables import Company,Queries,Chatbot_stats
from config.db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import datetime
from utils.query_utils import count_tokens

router = APIRouter(
    tags=['query']
)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", user_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

@router.post("/query")
async def answer_query(req: RequestModel,request :Request,db:db_dependency,user: dict = Depends(get_current_user)):
    try:
        collection_name = user.company_key
        chatbot_id = req.chatbot_id
        session_id = req.session_id
        print("Request Headers:", request.headers)

        origin_url = request.headers.get("origin")
        if origin_url is None:
            raise HTTPException(status_code=400, detail="Missing Origin Header")
        chatbot_stats = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id == req.chatbot_id).first()

        if not chatbot_stats:
            raise HTTPException(status_code=404,detail="Chatbot not found")

        if chatbot_stats.origin_url is None:
            raise HTTPException(status_code=500, detail="Chatbot origin URL is None")

        
        print("Chatbot Origin URL:", chatbot_stats.origin_url)
        print("Request Origin URL:", origin_url)

        if chatbot_stats.origin_url.strip() != origin_url.strip():
            raise HTTPException(status_code=401, detail="Unauthorized Domain")
        rag_chain = prompt | llm | StrOutputParser()
        with_message_history = RunnableWithMessageHistory(
            rag_chain,
            get_message_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        
        final_response = await with_message_history.ainvoke(
            {"context": context_retriever(req.query,session_id,user.id,chatbot_id,db,collection_name), "input": req.query,"chatbot_name":chatbot_stats.chatbot_name,"base_url":user.base_url},
            config={"configurable": {"session_id": req.session_id}},
        )

        
        history = get_message_history(req.session_id)


        query_model = db.query(Queries).filter(Queries.company_id == user.id,Queries.chatbot_id == req.chatbot_id, Queries.session_id == req.session_id,Queries.query_text_user == req.query).first()
        # Combine context, history, and user query into a single input string

        context = query_model.query_context
        combined_input = f"{context}\n{history}\n{req.query}"
        input_token = count_tokens(combined_input)+10
        output_token = count_tokens(final_response)

        query_model.query_text_bot = final_response
        query_model.query_time = query_model.query_time
        query_model.input_tokens = input_token
        query_model.output_tokens = output_token
        query_model.origin_url= origin_url


        chatbot_stats = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id == req.chatbot_id).first()
        if chatbot_stats:
            chatbot_stats.total_input_tokens += input_token
            chatbot_stats.total_output_tokens += output_token
            chatbot_stats.total_queries += 1
            chatbot_stats.last_query_time = datetime.datetime.now()     

        company = db.query(Company).filter(Company.id == user.id).first()
        if company:
            company.input_tokens += input_token
            company.output_tokens += output_token
        db.commit()

        return final_response
    except AttributeError as ae:
        print("AttributeError:", str(ae))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(ae)}")
    except Exception as e:
        print(e)
        # db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")