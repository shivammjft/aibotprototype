from mailjet_rest import Client
import os
from jinja2 import Template
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email_with_template(recipent_email, subject, company_name, base_link, chatbot_name, session_id,ip_address,chat_history,template):
    logger.info("Preparing to send email to %s", recipent_email)

    # Render the template with the provided values
    jinja_template = Template(template)
    html_content = jinja_template.render(
        company_name=company_name,
        base_link=base_link,
        chatbot_name=chatbot_name,
        session_id=session_id,
        ip_address=ip_address,
        chat_history=chat_history
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
