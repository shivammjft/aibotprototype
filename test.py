import time
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main_server.meetingScheduler import get_free_slots, create_event, send_email_with_template
from datetime import datetime
from google.oauth2 import service_account
import google.auth.transport.requests


app = FastAPI()


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


@app.post("/query")
async def query_dialogflow(req: QueryRequest):
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

        cancel_keywords = ["cancel", "stop", "exit", "I don't want", "never mind", "no thanks"]
        if any(keyword in req.query.lower() for keyword in cancel_keywords):
            return {
                "response": "Meeting scheduling has been canceled. Let me know if you need anything else.",
                "endInteraction": True  
            }
        if person_name and email and date and not time:
            email_list = [{"email": email}]
            date = convert_datetime_to_yyyy_mm_dd(date)
            free_slots = get_free_slots(email_list, date)

            if free_slots:
                return {
                    "response": f"Thanks for all the details {person_name.get('name')}. Our team is available for a meeting from {free_slots[0]['start']} to {free_slots[0]['end']}." + fulfillment_text,
                    "endInteraction": False
                }
            else:
                return {
                    "response": f"No available time slots on {date}. Please provide another date.",
                    "endInteraction": False
                }

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
                return {
                    "response": f"Meeting successfully scheduled for {person_name.get('name')} on {date} at {time}. You will receive a confirmation email shortly.",
                     "endInteraction": True
                }
            else:
                return {
                    "response": "There was an issue scheduling the meeting. Please try again later.",
                    "endInteraction": True
                }


        return {
            "response": fulfillment_text,
            "endInteraction": False
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# # from google.oauth2 import service_account
# # import google.auth.transport.requests

# # # Load your service account key
# # credentials = service_account.Credentials.from_service_account_file(
# #     'chatbot-meeting-scheduler-37092a8c0670.json',
# #     scopes=['https://www.googleapis.com/auth/dialogflow']  # Use the correct scope here
# # )

# # # Create a request object
# # request = google.auth.transport.requests.Request()

# # # Get the access token
# # credentials.refresh(request)
# # dialogflow_token = credentials.token

# # print(dialogflow_token)

# from langchain_core.output_parsers import StrOutputParser
# import logging
# from typing import Optional, List
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# load_dotenv()

# logger = logging.getLogger(__name__)

# llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# def check_meeting_intent(query: str, context: str) -> str:
#     prompt = (
#         """Does the provided user query indicate an intention to schedule a meeting or does the provided chat context suggest an ongoing meeting scheduling process? 
#         Respond with 'yes' if either is true; otherwise, respond with 'no'.

#         Query: {query}
#         Context: {context}
#         """
#     )
#     formatted_prompt = prompt.format(query=query, context=context)  
#     try:
#         response = llm.invoke(formatted_prompt)  
#         return response.content.lower()
#     except Exception as e:
#         logger.error("LLM Error: %s", str(e))
#         return "no"
    
# def concatenate_context(context: Optional[List[str]]) -> str:
#     if context is None:
#         return ""
    
#     formatted_strings = []
#     for i, statement in enumerate(context):
#         if i % 2 == 0:  
#             formatted_strings.append(f"User: {statement.strip()}")
#         else:  
#             formatted_strings.append(f"Bot: {statement.strip()}")
#     return "\n".join(formatted_strings)

# context = [
#     "i want to book a meeting",
#     "tell me your name",
#     "abhinav",
#     "tell me your email",
#     "abhinav99@gmail.com"
# ]

# res = check_meeting_intent("1 pm", concatenate_context(context))
# print(res) 