from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, OpenTracking
from jinja2 import Template
import logging
import os
import markdown
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_chat_html(chat_history):
    """Generate HTML content with dynamic chat history in the desired format."""
    chat_log_html = '<table style="width: 100%;">'

    for message in chat_history:
        if message["id"] == "bot":
            chat_class = "bot-message"
            alignment = ""
        else:
            chat_class = "user-message"
            alignment = 'style="text-align: right;"'

        message_html = markdown.markdown(message["message"])
        chat_log_html += f"""
        <tr>
          <td {alignment}>
            <div class="chat-bubble {chat_class}">
              {message_html}
            </div>
          </td>
        </tr>
        """

    chat_log_html += "</table>"
    return chat_log_html

def send_email_with_template(recipent_email, subject, company_name, base_link, chatbot_name, session_id, ip_address, chat_history, template):
    logger.info("Preparing to send email to %s", recipent_email)

    try: 
        jinja_template = Template(template)
        html_content = jinja_template.render(
            company_name=company_name,
            chat_log_html=generate_chat_html(chat_history),
            base_link=base_link,
            chatbot_name=chatbot_name,
            session_id=session_id,
            ip_address=ip_address,
            # chat_history=chat_history
        )
    except Exception as e:
        logger.error("Error rendering the email template: %s", e)
        return

    # Fetch environment variables
    sender_email = os.getenv('SENDER')
    api_key = os.getenv('SENDGRID_API_KEY')

    # Debug: Log sender email and partial API key
    logger.info("Sender Email: %s", sender_email)
    if api_key:
        logger.info("SendGrid API Key: %s", api_key[:6] + "..." + api_key[-4:])
    else:
        logger.error("SendGrid API Key is missing.")
        return

    if not sender_email or not api_key:
        logger.error("Missing sender email or SendGrid API key. Check your environment variables.")
        return

    # Create the email message
    message = Mail(
        from_email=sender_email,
        to_emails=recipent_email,
        subject=subject,
        plain_text_content="Greetings from Jellyfish Technologies!",
        html_content=html_content
    )

    # Optional: Add tracking settings (e.g., open tracking)
    tracking_settings = TrackingSettings()
    open_tracking = OpenTracking(enable=True)
    tracking_settings.open_tracking = open_tracking
    message.tracking_settings = tracking_settings

    # Send email using SendGrid
    logger.info("Sending email with subject: %s", subject)
    try:
        sg = SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        logger.info("Email sent successfully: Status Code = %s", response.status_code)
        logger.debug("Response body: %s", response.body)
    except Exception as e:
        logger.error("Failed to send email: %s", e)
        if hasattr(e, 'body'):
            logger.error("Error details: %s", e.body)
