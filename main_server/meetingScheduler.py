import os
import datetime as dt
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mailjet_rest import Client
from dotenv import load_dotenv
from jinja2 import Template
import uuid
from google.auth.transport.requests import Request
import logging
from dateutil.parser import parse

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def convert_ist_to_utc(event_date, event_time):
    ist = pytz.timezone('Asia/Kolkata')
    ist_datetime = dt.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
    ist_datetime = ist.localize(ist_datetime)
    utc_datetime = ist_datetime.astimezone(pytz.utc)
    return utc_datetime.isoformat()

def convert_utc_to_ist(utc_datetime_str):
    ist = pytz.timezone('Asia/Kolkata')
    utc_datetime = dt.datetime.fromisoformat(utc_datetime_str)
    ist_datetime = utc_datetime.astimezone(ist)
    return ist_datetime.strftime("%d %B %Y, %I:%M %p")


def get_free_slots(attendees, event_date):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            pass
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        event_start_utc = convert_ist_to_utc(event_date, "00:00")
        event_end_utc = convert_ist_to_utc(event_date, "23:59")

        body = {
            "timeMin": event_start_utc,
            "timeMax": event_end_utc,
            "timeZone": "UTC",
            "items": [{"id": attendee["email"]} for attendee in attendees]
        }

        freebusy_result = service.freebusy().query(body=body).execute()
        
        free_slots = []
        for attendee in attendees:
            email = attendee["email"]
            busy_periods = freebusy_result["calendars"][email]["busy"]

            free_start = dt.datetime.strptime(f"{event_date} 00:00", "%Y-%m-%d %H:%M").astimezone(pytz.utc)
            free_end = dt.datetime.strptime(f"{event_date} 23:59", "%Y-%m-%d %H:%M").astimezone(pytz.utc)

            for busy in busy_periods:
                busy_start = parse(busy["start"]).astimezone(pytz.utc)
                busy_end = parse(busy["end"]).astimezone(pytz.utc)
                
                if free_start < busy_start:
                    free_slots.append({
                        "start": free_start.isoformat(),
                        "end": busy_start.isoformat()
                    })
                free_start = busy_end

            if free_start < free_end:
                free_slots.append({
                    "start": free_start.isoformat(),
                    "end": free_end.isoformat()
                })

        free_slots_ist = []
        for slot in free_slots:
            free_slots_ist.append({
                "start": convert_utc_to_ist(slot['start']),
                "end": convert_utc_to_ist(slot['end'])
            })

        return free_slots_ist

    except HttpError as error:
        print(f"An error occurred: {error}")

def generate_request_id(attendee_email, event_date, event_time):
    unique_string = f"{attendee_email}_{event_date}_{event_time}_{uuid.uuid4()}"
    return unique_string.replace(" ", "").replace(":", "").replace("-", "")

def create_event(attendees, event_date, event_time):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)
        event_start_utc = convert_ist_to_utc(event_date, event_time)
        event_end_utc = convert_ist_to_utc(event_date, str(int(event_time[:2]) + 1).zfill(2) + event_time[2:])
        request_id = generate_request_id(attendees[0]["email"], event_date, event_time)

        event = {
            "summary": "Custom Event",
            "location": "Online",
            "description": "Event with Google Meet link.",
            "colorId": 6,
            "start": {
                "dateTime": event_start_utc,
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": event_end_utc,
                "timeZone": "UTC"
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": request_id,
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    }
                }
            },
            "attendees": attendees
        }

        event = service.events().insert(
            calendarId="primary",
            body=event,
            conferenceDataVersion=1
        ).execute()

        event_id = event["id"]
        event = service.events().get(calendarId="primary", eventId=event_id, ).execute()
        meeting_link = event['conferenceData']['entryPoints'][0]['uri']
        print("Meeting Link:", meeting_link)
        return meeting_link

    except HttpError as error:
        print(f"An error occurred: {error}")

def send_email_with_template(recipient_email, meeting_link):
    logger.info("Preparing to send email to %s", recipient_email)

    template = """
    <html>
        <body>
            <h1>Meeting Scheduled</h1>
            <p>Thank you for scheduling the meeting.</p>
            <p>Your meeting link: <a href="{{ meeting_link }}">{{ meeting_link }}</a></p>
        </body>
    </html>
    """

    jinja_template = Template(template)
    html_content = jinja_template.render(meeting_link=meeting_link)

    sender_email = os.getenv("SENDER_EMAIL")
    api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_SECRET_KEY")
    
    logger.info("Initializing Mailjet client")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Jellyfish Technologies"
                },
                "To": [
                    {
                        "Email": recipient_email,
                        "Name": "Recipient"
                    }
                ],
                "Subject": "Your Meeting Link",
                "TextPart": "Thank you for scheduling the meeting!",
                "HTMLPart": html_content
            }
        ]
    }
    
    logger.info("Sending email with subject: %s", "Your Meeting Link")
    try:
        result = mailjet.send.create(data=data)
        logger.info("Email sent successfully: %s", result.json())
    except Exception as e:
        logger.error("Failed to send email: %s", e)


def schedule_meeting():
    name = input("Please enter your name: ")
    email = input(f"Hi {name}! Please enter your email: ")
    event_date = input("Please enter the date for the meeting (YYYY-MM-DD): ")
    attendees = [{"email": email}]
    free_slots = get_free_slots(attendees, event_date)
    print("Free slots for the day (IST):")
    for idx, slot in enumerate(free_slots):
        print(f"{idx + 1}. Start: {slot['start']}, End: {slot['end']}")
    meeting_time = input("Please enter the meeting time in HH:MM format (24-hour): ")
    meeting_link = create_event(attendees, event_date, meeting_time)
    send_email_with_template(email, "Your Meeting Link", meeting_link)

if __name__ == "__main__":
    schedule_meeting()


# from flask import Flask, request, jsonify, send_from_directory
# import uuid
# import os
# import datetime as dt
# import pytz
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from dateutil.parser import parse
# # from mailjet_rest import Client
# from dotenv import load_dotenv
# from jinja2 import Template
# import logging
# from google.auth.transport.requests import Request
# from collections import defaultdict

# app = Flask(__name__)

# user_sessions = {}

# load_dotenv()

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# SCOPES = ["https://www.googleapis.com/auth/calendar"]

# def convert_ist_to_utc(event_date, event_time):
#     ist = pytz.timezone('Asia/Kolkata')
#     ist_datetime = dt.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
#     ist_datetime = ist.localize(ist_datetime)
#     utc_datetime = ist_datetime.astimezone(pytz.utc)
#     return utc_datetime.isoformat()

# def convert_utc_to_ist(utc_datetime_str):
#     ist = pytz.timezone('Asia/Kolkata')
#     utc_datetime = dt.datetime.fromisoformat(utc_datetime_str)
#     ist_datetime = utc_datetime.astimezone(ist)
#     return ist_datetime.strftime("%d %B %Y, %I:%M %p")

# def get_free_slots(user_email, event_date):
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json")

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("calendar", "v3", credentials=creds)
#         event_start_utc = convert_ist_to_utc(event_date, "00:00")
#         event_end_utc = convert_ist_to_utc(event_date, "23:59")

#         body = {
#             "timeMin": event_start_utc,
#             "timeMax": event_end_utc,
#             "timeZone": "UTC",
#             "items": [{"id": user_email}]
#         }

#         freebusy_result = service.freebusy().query(body=body).execute()
#         busy_periods = freebusy_result["calendars"][user_email]["busy"]

#         free_slots = []
#         free_start = dt.datetime.strptime(f"{event_date} 00:00", "%Y-%m-%d %H:%M").astimezone(pytz.utc)
#         free_end = dt.datetime.strptime(f"{event_date} 23:59", "%Y-%m-%d %H:%M").astimezone(pytz.utc)

#         for busy in busy_periods:
#             busy_start = parse(busy["start"]).astimezone(pytz.utc)
#             busy_end = parse(busy["end"]).astimezone(pytz.utc)

#             if free_start < busy_start:
#                 free_slots.append({
#                     "start": free_start.isoformat(),
#                     "end": busy_start.isoformat()
#                 })
#             free_start = busy_end

#         if free_start < free_end:
#             free_slots.append({
#                 "start": free_start.isoformat(),
#                 "end": free_end.isoformat()
#             })

#         free_slots_ist = []
#         for slot in free_slots:
#             free_slots_ist.append({
#                 "start": convert_utc_to_ist(slot['start']),
#                 "end": convert_utc_to_ist(slot['end'])
#             })

#         return free_slots_ist

#     except HttpError as error:
#         print(f"An error occurred: {error}")

# def generate_request_id(attendee_email, event_date, event_time):
#     unique_string = f"{attendee_email}_{event_date}_{event_time}_{uuid.uuid4()}"
#     return unique_string.replace(" ", "").replace(":", "").replace("-", "")

# def create_event(user_email, event_date, event_time):
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json")

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("calendar", "v3", credentials=creds)
#         event_start_utc = convert_ist_to_utc(event_date, event_time)
#         event_end_utc = convert_ist_to_utc(event_date, str(int(event_time[:2]) + 1).zfill(2) + event_time[2:])
#         request_id = generate_request_id(user_email, event_date, event_time)

#         event = {
#             "summary": "Custom Event",
#             "location": "Online",
#             "description": "Event with Google Meet link.",
#             "colorId": 6,
#             "start": {
#                 "dateTime": event_start_utc,
#                 "timeZone": "UTC"
#             },
#             "end": {
#                 "dateTime": event_end_utc,
#                 "timeZone": "UTC"
#             },
#             "conferenceData": {
#                 "createRequest": {
#                     "requestId": request_id,
#                     "conferenceSolutionKey": {
#                         "type": "hangoutsMeet"
#                     }
#                 }
#             },
#             "attendees": [{"email": user_email}]
#         }

#         event = service.events().insert(
#             calendarId="primary",
#             body=event,
#             conferenceDataVersion=1
#         ).execute()

#         event_id = event["id"]
#         event = service.events().get(calendarId="primary", eventId=event_id).execute()
#         meeting_link = event['conferenceData']['entryPoints'][0]['uri']
#         print("Meeting Link:", meeting_link)
#         return meeting_link

#     except HttpError as error:
#         print(f"An error occurred: {error}")

# def send_email_with_template(recipient_email, subject, meeting_link):
#     logger.info("Preparing to send email to %s", recipient_email)

#     template = """
#     <html>
#         <body>
#             <h1>Meeting Scheduled</h1>
#             <p>Thank you for scheduling the meeting.</p>
#             <p>Your meeting link: <a href="{{ meeting_link }}">{{ meeting_link }}</a></p>
#         </body>
#     </html>
#     """

#     jinja_template = Template(template)
#     html_content = jinja_template.render(meeting_link=meeting_link)

#     sender_email = os.getenv("SENDER_EMAIL")
#     api_key = os.getenv("MAILJET_API_KEY")
#     api_secret = os.getenv("MAILJET_SECRET_KEY")
    
#     logger.info("Initializing Mailjet client")
#     mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
#     data = {
#         'Messages': [
#             {
#                 "From": {
#                     "Email": sender_email,
#                     "Name": "Jellyfish Technologies"
#                 },
#                 "To": [
#                     {
#                         "Email": recipient_email,
#                         "Name": "Recipient"
#                     }
#                 ],
#                 "Subject": "Your Meeting Link",
#                 "TextPart": "Thank you for scheduling the meeting!",
#                 "HTMLPart": html_content
#             }
#         ]
#     }
    
#     logger.info("Sending email with subject: %s", "Your Meeting Link")
#     try:
#         result = mailjet.send.create(data=data)
#         logger.info("Email sent successfully: %s", result.json())
#     except Exception as e:
#         logger.error("Failed to send email: %s", e)

# user_sessions = defaultdict(dict)

# async def ask_user_data(session_id: str, user_input: str):
#     user_data = user_sessions.get(session_id, {})

#     if user_input.lower() == "cancel":
#         return "Meeting scheduling canceled."

#     if 'email' not in user_data:
#         return "Please provide your email address:"

#     if 'name' not in user_data:
#         user_data['email'] = user_input
#         return "Thank you! What is your name?"

#     if 'date' not in user_data:
#         user_data['name'] = user_input
#         return f"Great, {user_data['name']}! What date do you want to schedule a meeting? (YYYY-MM-DD)"

#     if 'date' not in user_data:
#         user_data['date'] = user_input
#         free_slots = get_free_slots(user_data['email'], user_data['date'])

#         if not free_slots:
#             return "No free slots available for the provided date. Please provide a new date:"

#         user_data['free_slots'] = free_slots
#         slot_options = "\n".join([f"{slot['start']} to {slot['end']}" for slot in free_slots])
#         return f"Here are the available slots:\n{slot_options}\nPlease provide a time from the above slots (e.g., HH:MM):"

#     if 'time' not in user_data:
#         user_data['time'] = user_input
#         meeting_link = create_event(user_data['email'], user_data['date'], user_data['time'])

#         send_email_with_template(user_data['email'], "Your Meeting Link", meeting_link)

#         return "Meeting scheduled successfully! Here is your meeting link: " + meeting_link

#     return "Invalid input."
