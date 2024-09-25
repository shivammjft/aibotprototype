from mailjet_rest import Client
from dotenv import load_dotenv
import os
from jinja2 import Template
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email_with_template(recipent_email, subject, company_id, company_name, base_link, API_KEY, CHATBOT_KEY, chatbot_name, template):
    logger.info("Preparing to send email to %s", recipent_email)

    # Render the template with the provided values
    jinja_template = Template(template)
    html_content = jinja_template.render(
        company_id=company_id,
        company_name=company_name,
        base_link=base_link,
        API_KEY=API_KEY,
        CHATBOT_KEY=CHATBOT_KEY,
        chatbot_name=chatbot_name
    )
    
    sender_email = os.getenv('SENDER')
    api_key = os.environ['MAILJET_API_KEY']
    api_secret = os.environ['MAILJET_SECRET_KEY']
    
    logger.info("Initializing Mailjet client")
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    data = {
        'Messages': [
            {
                "From": {
                    "Email": sender_email,
                    "Name": "Me"
                },
                "To": [
                    {
                        "Email": recipent_email,
                        "Name": "You"
                    }
                ],
                "Subject": subject,
                "TextPart": "Greetings from Jellyfish Technologies!",
                "HTMLPart": html_content
            }
        ]
    }
    
    logger.info("Sending email with subject: %s", subject)
    try:
        result = mailjet.send.create(data=data)
        logger.info("Email sent successfully: %s", result.json())
    except Exception as e:
        logger.error("Failed to send email: %s", e)
