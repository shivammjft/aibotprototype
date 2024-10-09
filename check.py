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
from flask import Flask, request, jsonify
from dateutil.parser import parse
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Calendar API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = Flask(__name__)

def convert_ist_to_utc(event_date, event_time):
    """Convert IST date and time to UTC ISO format."""
    ist = pytz.timezone('Asia/Kolkata')
    ist_datetime = dt.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
    ist_datetime = ist.localize(ist_datetime)
    utc_datetime = ist_datetime.astimezone(pytz.utc)
    return utc_datetime.isoformat()

def convert_utc_to_ist(utc_datetime_str):
    """Convert UTC ISO format to IST date and time string."""
    ist = pytz.timezone('Asia/Kolkata')
    utc_datetime = dt.datetime.fromisoformat(utc_datetime_str)
    ist_datetime = utc_datetime.astimezone(ist)
    return ist_datetime.strftime("%d %B %Y, %I:%M %p")

def get_free_slots(attendees, event_date):
    """Get free time slots for the attendees on the specified date."""
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
        logger.error(f"An error occurred: {error}")
        return []

def generate_request_id(attendee_email, event_date, event_time):
    """Generate a unique request ID for the event."""
    unique_string = f"{attendee_email}_{event_date}_{event_time}_{uuid.uuid4()}"
    return unique_string.replace(" ", "").replace(":", "").replace("-", "")

def create_event(attendees, event_date, event_time):
    """Create an event in Google Calendar."""
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
        event = service.events().get(calendarId="primary", eventId=event_id).execute()
        meeting_link = event['conferenceData']['entryPoints'][0]['uri']
        logger.info("Meeting Link: %s", meeting_link)
        return meeting_link

    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        return None

def send_email_with_template(recipient_email, meeting_link):
    """Send an email with the meeting link to the recipient."""
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

@app.route('/get_free_slots', methods=['POST'])
def api_get_free_slots():
    """API endpoint to get free slots."""
    data = request.json
    attendees = data.get('attendees')
    event_date = data.get('event_date')

    if not attendees or not event_date:
        return jsonify({"error": "Attendees and event date are required"}), 400
    
    free_slots = get_free_slots(attendees, event_date)
    return jsonify({"free_slots": free_slots}), 200

@app.route('/schedule_meeting', methods=['POST'])
def api_schedule_meeting():
    """API endpoint to schedule a meeting."""
    data = request.json
    attendees = data.get('attendees')
    event_date = data.get('event_date')
    event_time = data.get('event_time')

    if not attendees or not event_date or not event_time:
        return jsonify({"error": "Attendees, event date, and event time are required"}), 400

    meeting_link = create_event(attendees, event_date, event_time)

    if not meeting_link:
        return jsonify({"error": "Failed to create the meeting"}), 500
    
    for attendee in attendees:
        send_email_with_template(attendee['email'], meeting_link)

    return jsonify({"meeting_link": meeting_link}), 201

if __name__ == '__main__':
    app.run(debug=True)
