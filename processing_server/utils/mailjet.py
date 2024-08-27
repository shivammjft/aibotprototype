from mailjet_rest import Client
from dotenv import load_dotenv
import os 
from jinja2 import Template


def send_email_with_template(recipent_email,subject,company_id,company_name,base_link,API_KEY,chatbot_name,template):
    template = Template(template)
        # Render the template with the provided values
    html_content = template.render(
            company_id=company_id,
            company_name=company_name,
            base_link=base_link,
            API_KEY=API_KEY,
            chatbot_name=chatbot_name
        )
    sender_email = os.getenv('SENDER')
    api_key = os.environ['MAILJET_API_KEY']
    api_secret = os.environ['MAILJET_SECRET_KEY']
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
    result = mailjet.send.create(data=data)
    print(result)