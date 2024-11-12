from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from utils.auth import get_current_user
from utils.query_utils import llm, get_message_history, context_retriever,escape_template_string
from constants.prompts import user_message
from models.schemas import RequestModel ,SendChat, AddVisitorRequest
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from models.tables import Company, Queries, Chatbot_stats, QueryUsers
from config.db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import datetime
from utils.query_utils import count_tokens,meeting_finder
import logging
import traceback
from constants.email import bot_chat_template
from utils.mailket_utils import send_email_with_template
router = APIRouter(tags=['query'])

tools=[]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



@router.post("/query")
async def answer_query(req: RequestModel, request: Request, db: db_dependency, user: dict = Depends(get_current_user)):
    try:
        collection_name = user.company_key
        chatbot_id = req.chatbot_id
        session_id = req.session_id
        logger.info("Chatbot ID: %s", req.chatbot_id)
        logger.info("Session ID: %s", req.session_id)
        logger.info("Company Key: %s", user.company_key)

        logger.info("Request Headers: %s", request.headers)

        origin_url = request.headers.get("origin")
        if origin_url is None:
            logger.error("Missing Origin Header")
            raise HTTPException(status_code=400, detail="Missing Origin Header")

        chatbot_stats = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id == req.chatbot_id).first()
        if not chatbot_stats:
            logger.error("Chatbot not found: %s", req.chatbot_id)
            raise HTTPException(status_code=404, detail="Chatbot not found")

        logger.info("Prompt tmeplate: Type %s", type(chatbot_stats.chatbot_prompt))

        promt_template = chatbot_stats.chatbot_prompt

        logger.info("Prompt tmeplate: %s", promt_template)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", promt_template),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )


        if chatbot_stats.origin_url is None:
            logger.error("Chatbot origin URL is None")
            raise HTTPException(status_code=500, detail="Chatbot origin URL is None")

        logger.info("Chatbot Origin URL: %s", chatbot_stats.origin_url)
        logger.info("Request Origin URL: %s", origin_url)

        if chatbot_stats.origin_url.strip() != origin_url.strip():
            logger.warning("Unauthorized Domain: %s", origin_url)
            raise HTTPException(status_code=401, detail="Unauthorized Domain")
        
        rag_chain = prompt | llm | StrOutputParser()

        with_message_history = RunnableWithMessageHistory(
            rag_chain,
            get_message_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        final_response = await with_message_history.ainvoke(
            {
                "context": context_retriever(req.query, session_id, user.id, chatbot_id, db, collection_name),
                "input": req.query,
                "chatbot_name": chatbot_stats.chatbot_name,
                "base_url": user.base_url,
            },
            config={"configurable": {"session_id": req.session_id}},
        )


        history = get_message_history(req.session_id)
        if history is None:
            logger.error("Message history retrieval failed for session ID: %s", req.session_id)
            raise HTTPException(status_code=500, detail="Message history retrieval failed")

        query_model = db.query(Queries).filter(
            Queries.company_id == user.id,
            Queries.chatbot_id == req.chatbot_id,
            Queries.session_id == req.session_id,
            Queries.query_text_user == req.query
        ).first()

        if query_model is None:
            logger.error("Query not found for user ID: %s, chatbot ID: %s, session ID: %s", user.id, req.chatbot_id, req.session_id)
            raise HTTPException(status_code=404, detail="Query not found")

        context = query_model.query_context
        if context is None:
            logger.error("Query context is None for session ID: %s", req.session_id)
            raise HTTPException(status_code=500, detail="Query context is None")

        combined_input = f"{context}\n{history}\n{req.query}"
        input_token = count_tokens(combined_input) + 10
        output_token = count_tokens(final_response)

        query_model.query_text_bot = final_response
        query_model.input_tokens = input_token
        query_model.output_tokens = output_token
        query_model.origin_url = origin_url

        chatbot_stats.total_input_tokens += input_token
        chatbot_stats.total_output_tokens += output_token
        chatbot_stats.total_queries += 1
        chatbot_stats.last_query_time = datetime.datetime.now()

   
        company = db.query(Company).filter(Company.id == user.id).first()
        if company:
            company.input_tokens += input_token
            company.output_tokens += output_token
        
        db.commit()
        logger.info("Successfully processed query for user ID: %s", user.id)

        return final_response
    except AttributeError as ae:
        logger.error("AttributeError: %s", str(ae))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(ae)}")
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        db.rollback()  # Rollback on error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/send-chat/")
def send_chat_email(req: SendChat, request: Request, db: db_dependency,user: dict = Depends(get_current_user)):
    try:
        logger.info("Incoming Request: %s", request)
        chatbot_id = req.chatbot_id
        session_id = req.session_id
        chat_history = req.chatHistory
        logger.info("Chatbot ID: %s", req.chatbot_id)
        logger.info("Session ID: %s", req.session_id)



        ip_address = request.client.host
        logger.info("Incoming Request Ip: %s", ip_address)
        print(ip_address)
        origin_url = request.headers.get("origin")
        if origin_url is None:
            logger.error("Missing Origin Header")
            raise HTTPException(status_code=400, detail="Missing Origin Header")
        
        chatbot_stats = db.query(Chatbot_stats).filter(Chatbot_stats.chatbot_id == chatbot_id).first()
        if not chatbot_stats:
            logger.error("Chatbot not found: %s", req.chatbot_id)
            raise HTTPException(status_code=404, detail="Chatbot not found")

        email = 'info@jellyfishtechnologies.com'
        send_email_with_template(
            recipent_email=email,
            subject="Chatbot Chat",
            company_name=user.company_name,
            base_link=chatbot_stats.origin_url,
            chatbot_name=chatbot_stats.chatbot_name,
            session_id=session_id,
            ip_address=ip_address,
            chat_history=chat_history,
            template=bot_chat_template
        )

        return JSONResponse(content={"status": "200", 'message': 'Email sent successfully'})

    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.post("/add-visitor/")
def add_visitor(req: AddVisitorRequest, request: Request,db:db_dependency):
    try:
        ip_address = request.client.host
        logger.info("Incoming Request: %s", req)
        logger.info("Origin URL: %s, Session ID: %s,IP Address: %s" , req.origin_url, req.session_id,ip_address)
        
        new_visitor = QueryUsers(
            session_id=req.session_id,
            chatbot_id=req.chatbot_id,
            ip_address=ip_address,
            origin_url=req.origin_url,
            timezone=req.timezone,
            language=req.language,
            is_mobile=req.is_mobile,
            user_agent=req.user_agent,
            platform=req.platform,
            referrer=req.referrer,
            location=req.location,
            network_type=req.network_type
        )

        db.add(new_visitor)
        db.commit()
        
        return {"status": "200", "message": "Visitor successfully added"}

    except Exception as e:
        # Rollback transaction if error occurs
        logger.error("An unexpected error occurred: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")