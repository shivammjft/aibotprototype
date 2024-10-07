from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils.auth import get_current_user
from utils.query_utils import llm, get_message_history, context_retriever
from models.schems import RequestModel ,SendChat
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from models.tables import Company, Queries, Chatbot_stats
from config.db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
from utils.query_utils import count_tokens
import logging
import traceback
from constants.email import bot_chat_template
from typing import Optional, List
from google.oauth2 import service_account
import google.auth.transport.requests
import time
import requests
from meetingScheduler import get_free_slots, create_event, send_email_with_template
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

MEETING_KEYWORDS = [
    "meeting", "schedule", "appointment", "book", "plan",
    "arrange", "set up", "organize", "conference", "session",
    "discussion", "call", "touch base", "catch up", "coordinate"
]

def contains_meeting_keyword(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in MEETING_KEYWORDS)

def check_meeting_intent(query: str, context: str) -> str:
    prompt = (
        """Does the provided user query indicate an intention to schedule a meeting or does the provided chat context suggest an ongoing meeting scheduling process? 
        Respond with 'yes' if either is true; otherwise, respond with 'no'.

        Query: {query}
        Context: {context}
        """
    )
    formatted_prompt = prompt.format(query=query, context=context)  
    try:
        response = llm.invoke(formatted_prompt)  
        return response.content.lower().strip()
    except Exception as e:
        logger.error("LLM Error: %s", str(e))
        return "no"
    
def concatenate_context(context: Optional[List[str]], query: str) -> str:
    if context is None:
        return ""
    formatted_strings = []
    for i, statement in enumerate(context):
        if i % 2 == 0:  
            formatted_strings.append(f"User: {statement.strip()}")
        else:  
            formatted_strings.append(f"Bot: {statement.strip()}")
    formatted_strings.append(f"User: {query}")
    return "\n".join(formatted_strings)

DIALOGFLOW_PROJECT_ID = "chatbot-meeting-scheduler"
DIALOGFLOW_URL = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions"


credentials = service_account.Credentials.from_service_account_file(
    'chatbot-meeting-scheduler-37092a8c0670.json',
    scopes=['https://www.googleapis.com/auth/dialogflow']
)

request = google.auth.transport.requests.Request()

DIALOGFLOW_TOKEN = None
TOKEN_EXPIRATION_TIME = 0

def get_dialogflow_token():
    global DIALOGFLOW_TOKEN, TOKEN_EXPIRATION_TIME

    if DIALOGFLOW_TOKEN is None or TOKEN_EXPIRATION_TIME is None or time.time() >= TOKEN_EXPIRATION_TIME:
        credentials.refresh(request)
        DIALOGFLOW_TOKEN = credentials.token
        
        TOKEN_EXPIRATION_TIME = credentials.expiry.timestamp()  

    return DIALOGFLOW_TOKEN


class QueryRequest(BaseModel):
    query: str
    session_id: str

def convert_datetime_to_yyyy_mm_dd(datetime_str):
    dt_object = datetime.fromisoformat(datetime_str)
    formatted_date = dt_object.strftime('%Y-%m-%d')
    return formatted_date

def convert_to_hh_mm(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%H:%M")

CHECK_KEYS = ["Meeting successfully scheduled for", "There was an issue scheduling the meeting. Please try again later.", "Meeting scheduling has been canceled. Let me know if you need anything else."]

def contains_check_keyword(context: str, phrases: list) -> bool:
    if not isinstance(context, str):
        raise ValueError("The context must be a string.")
    if not isinstance(phrases, list):
        raise ValueError("The phrases must be a list of strings.")
    return any(phrase in context for phrase in phrases)



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
        
        if chatbot_stats.origin_url is None:
            logger.error("Chatbot origin URL is None")
            raise HTTPException(status_code=500, detail="Chatbot origin URL is None")
        
        if contains_meeting_keyword(concatenate_context(req.context, req.query)) and not contains_check_keyword(concatenate_context(req.context, req.query), CHECK_KEYS):
            logger.info(not contains_check_keyword(concatenate_context(req.context, req.query), CHECK_KEYS))
            logger.info("Meeting-related keyword detected in query.")
            intent = check_meeting_intent(req.query, concatenate_context(req.context, req.query))
            logger.info("Meeting intent determined by LLM: %s", intent)
            if intent == 'yes':
                try: 
                    DIALOGFLOW_TOKEN = get_dialogflow_token()
                    url = f"{DIALOGFLOW_URL}/{req.session_id}:detectIntent"
                    
                    headers = {
                        "Authorization": f"Bearer {DIALOGFLOW_TOKEN}",
                        "Content-Type": "application/json"
                    }
                    
                    body = {
                        "queryInput": {
                            "text": {
                                "text": req.query,
                                "languageCode": "en" 
                            }
                        }
                    }

                    response = requests.post(url, headers=headers, json=body)
                    
                    if response.status_code != 200:
                        raise HTTPException(status_code=response.status_code, detail="Error communicating with Dialogflow")

                    dialogflow_response = response.json()
                    fulfillment_text = dialogflow_response.get('queryResult', {}).get('fulfillmentText', '')
                    parameters = dialogflow_response.get('queryResult', {}).get('parameters', {})
                    person_name = parameters.get('person', '')
                    email = parameters.get('email', '')
                    date = parameters.get('date', '')
                    time = parameters.get('time', '') 

                    cancel_keywords = ["cancel", "stop", "exit", "leave it", "never mind", "no thanks"]
                    if any(keyword in req.query.lower() for keyword in cancel_keywords):
                        return "Meeting scheduling has been canceled. Let me know if you need anything else."
                        
                    if person_name and email and date and not time:
                        email_list = [{"email": email}]
                        date = convert_datetime_to_yyyy_mm_dd(date)
                        free_slots = get_free_slots(email_list, date)

                        if free_slots:
                            return f"Thanks for all the details {person_name.get('name')}. Our team is available for a meeting from {free_slots[0]['start']} to {free_slots[0]['end']}." + fulfillment_text,
                            
                        else:
                            return f"No available time slots on {date}. Please provide another date."

                    elif person_name and email and date and time:
                        email_list = [{"email": email}]
                        date = convert_datetime_to_yyyy_mm_dd(date)
                        print(time)
                        time = convert_to_hh_mm(time)
                        print(time)
                        meeting_link = create_event(email_list, date, time)
                        print(meeting_link)
                        if meeting_link:
                            send_email_with_template(email, meeting_link)
                            return f"Meeting successfully scheduled for {person_name.get('name')} on {date} at {time}. You will receive a confirmation email shortly.",   
                        else:
                            return "There was an issue scheduling the meeting. Please try again later."


                    return fulfillment_text

                except Exception as e:
                    print(e)
                    raise HTTPException(status_code=500, detail=str(e)) 

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
        chatbot_stats.last_query_time = datetime.now()

   
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
    