import openai
import json
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

client = openai.OpenAI(
    base_url="https://api.deepinfra.com/v1/openai",
    api_key=os.getenv("DEEP_INFRA_API_KEY"),
)



load_dotenv()

# Set up logging
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

def generate_request_id(attendee_email, event_date, event_time):
    """
    Generate a unique request_id for Google Meet link generation.

    This id is used as the `requestId` in the Google Meet API request.
    It is a combination of the attendee's email, event date, event time, and a uuid4.

    :param attendee_email: The email address of the attendee.
    :param event_date: The date of the event in "YYYY-MM-DD" format.
    :param event_time: The time of the event in "HH:MM" format.
    :return: A unique request_id as a string.
    """
    unique_string = f"{attendee_email}_{event_date}_{event_time}_{uuid.uuid4()}"
    return unique_string.replace(" ", "").replace(":", "").replace("-", "")


def get_free_slots(attendees, event_date):
    """
    Get free slots for a given list of attendees on a given date.

    The function takes a list of attendees and a date, and returns a list of free slots
    for the attendees on that date. The free slots are returned in the format
    ``[{"start": "YYYY-MM-DD HH:MM", "end": "YYYY-MM-DD HH:MM"}]``.

    The function uses the Google Calendar API to get the free/busy information for the
    attendees and then calculates the free slots by finding the gaps in the busy
    periods.

    :param attendees: A list of dictionaries with the email address of each attendee.
    :param event_date: The date to find the free slots for in "YYYY-MM-DD" format.
    :return: A list of free slots in the format ``[{"start": "YYYY-MM-DD HH:MM", "end": "YYYY-MM-DD HH:MM"}]``.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # creds.refresh(Request())
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



def create_event(attendees, event_date, event_time):
    """
    Create a Google Calendar event and return the Google Meet link.

    :param attendees: List of dictionaries with "email" and "name" keys.
    :param event_date: Date of the event in "YYYY-MM-DD" format.
    :param event_time: Time of the event in "HH:MM" format.
    :return: The Google Meet link for the created event.
    """
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

def send_email_with_template(recipient_email, subject, meeting_link):
    """
    Send an email with a meeting link to the recipient.

    :param recipient_email: Email address of the recipient.
    :param subject: Subject of the email.
    :param meeting_link: Meeting link to be shared in the email.
    """
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

    sender_email = 'shivam.pandey@jellyfishtechnologies.com'
    api_key = 'b206a37878213791ca36f654de1a5ee4'
    api_secret = '0186662647f8ca1a38953139ce28ff3a'
    
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

# def schedule_meeting():
#     name = input("Please enter your name: ")
#     email = input(f"Hi {name}! Please enter your email: ")
#     event_date = input("Please enter the date for the meeting (YYYY-MM-DD): ")
#     attendees = [{"email": email}]
#     free_slots = get_free_slots(attendees, event_date)
#     print("Free slots for the day (IST):")
#     for idx, slot in enumerate(free_slots):
#         print(f"{idx + 1}. Start: {slot['start']}, End: {slot['end']}")
#     meeting_time = input("Please enter the meeting time in HH:MM format (24-hour): ")
#     meeting_link = create_event(attendees, event_date, meeting_time)
#     send_email_with_template(email, "Your Meeting Link", meeting_link)


    
def get_current_weather(location):
    """Get the current weather in a given location"""
    print("Calling get_current_weather client side.")
    if "tokyo" in location.lower():
        return json.dumps({
            "location": "Tokyo",
            "temperature": "75"
        })
    elif "san francisco" in location.lower():
        return json.dumps({
            "location": "San Francisco",
            "temperature": "60"
        })
    elif "paris" in location.lower():
        return json.dumps({
            "location": "Paris",
            "temperature": "70"
        })
    else:
        return json.dumps({"location": location, "temperature": "unknown"})



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_free_slots",
            "description": "Get free slots for a given list of attendees on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "attendees": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "description": "Email address of the attendee."
                                }
                            },
                            "required": ["email"]
                        },
                        "description": "List of attendees with their email addresses."
                    },
                    "event_date": {
                        "type": "string",
                        "description": "Date to find free slots for in 'YYYY-MM-DD' format."
                    }
                },
                "required": ["attendees", "event_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Create a Google Calendar event and return the Google Meet link.",
            "parameters": {
                "type": "object",
                "properties": {
                    "attendees": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "description": "Email address of the attendee."
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Name of the attendee."
                                }
                            },
                            "required": ["email", "name"]
                        },
                        "description": "List of attendees with their email addresses and names."
                    },
                    "event_date": {
                        "type": "string",
                        "description": "Date of the event in 'YYYY-MM-DD' format."
                    },
                    "event_time": {
                        "type": "string",
                        "description": "Time of the event in 'HH:MM' format."
                    }
                },
                "required": ["attendees", "event_date", "event_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email_with_template",
            "description": "Send an email with a meeting link to the recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_email": {
                        "type": "string",
                        "description": "Email address of the recipient."
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject of the email."
                    },
                    "meeting_link": {
                        "type": "string",
                        "description": "Meeting link to be shared in the email."
                    }
                },
                "required": ["recipient_email", "subject", "meeting_link"]
            }
        }
    }
]





async def meeting_tool_calls_handler(messages):
    response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    )
    tool_calls = response.choices[0].message.tool_calls

    messages.append(response.choices[0].message)

    for tool_call in tool_calls:
      function_name = tool_call.function.name
      if function_name == "get_current_weather":
          function_args = json.loads(tool_call.function.arguments)
          function_response = get_current_weather(
              location=function_args.get("location")
          )

    messages.append(
    {
        "role": "user",
        "content": "Gather all the informations that are required for the function call to schedule the meeting."
    }   )
    
    messages.append({
          "tool_call_id": tool_call.id,
          "role": "tool",
          "content": function_response,
      })  

    second_response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    messages=messages,
    tools=tools,
    tool_choice="auto",
        )  

    return(second_response.choices[0].message.content)
    
    