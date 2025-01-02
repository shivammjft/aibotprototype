# bot_chat_template = """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Chat Logs from Your AI Chatbot</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             background-color: #f5f5f5;
#             margin: 0;
#             padding: 0;
#         }
#         .container {
#             max-width: 800px;
#             margin: 40px auto;
#             background: #fff;
#             border-radius: 8px;
#             box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
#             overflow: hidden;
#         }
#         .header {
#             background: #007BFF;
#             color: white;
#             padding: 20px;
#             text-align: center;
#         }
#         .header h1 {
#             margin: 0;
#             font-size: 1.5em;
#         }
#         .details {
#             background: #f1f1f1;
#             padding: 15px;
#             border-bottom: 1px solid #ddd;
#         }
#         .details p {
#             margin: 5px 0;
#             font-size: 0.9em;
#             color: #333;
#         }
#         .chat-log {
#             padding: 20px;
#         }
#         .message {
#             display: flex;
#             margin-bottom: 15px;
#         }
#         .message.user {
#             justify-content: flex-end;
#         }
#         .message.bot {
#             justify-content: flex-start;
#         }
#         .message-content {
#             max-width: 70%;
#             padding: 10px 15px;
#             border-radius: 15px;
#             font-size: 0.9em;
#             line-height: 1.4;
#         }
#         .message.user .message-content {
#             background: #007BFF;
#             color: white;
#         }
#         .message.bot .message-content {
#             background: #e9f7ef;
#             color: #333;
#         }
#         .footer {
#             background: #f1f1f1;
#             text-align: center;
#             padding: 10px;
#             font-size: 0.8em;
#             color: #666;
#             border-top: 1px solid #ddd;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>Chat Logs from Your AI Chatbot</h1>
#         </div>

#         <div class="details">
#             <p><strong>Company Name:</strong> {{ company_name }}</p>
#             <p><strong>Chatbot Name:</strong> {{ chatbot_name }}</p>
#             <p><strong>Session ID:</strong> {{ session_id }}</p>
#             <p><strong>IP Address:</strong> {{ ip_address }}</p>
#             <p><strong>Deployed URL:</strong> <a href="{{ base_link }}" target="_blank">{{ base_link }}</a></p>
#         </div>

#         <div class="chat-log">
#             {% for message in chat_history %}
#                 <div class="message {{ message.id }}">
#                     <div class="message-content">{{ message.message }}</div>
#                 </div>
#             {% endfor %}
#         </div>

#         <div class="footer">
#             <p>Thank you for using our AI chatbot service!</p>
#         </div>
#     </div>
# </body>
# </html>

# """


bot_chat_template ="""

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Chat Logs from Your AI Chatbot</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #d9e8ff;
        margin: 0;
        padding: 0;
      }
      .container {
        max-width: 800px;
        margin: 40px auto;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        overflow: hidden;
      }
      .header {
        background: linear-gradient(90deg, #0056b3, #007bff);
        color: white;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
      }
      .details {
        background: #eaf3ff;
        padding: 15px;
        border-bottom: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        font-size: 0.9em;
        color: #333;
      }
      .details p {
        margin: 5px 0;
      }
      .details a {
        color: #0056b3;
        text-decoration: none;
      }
      .chat-log {
        padding: 20px;
        background: #f7fbff;
        max-height: 400px;
        overflow-y: auto;
      }
      .chat-message {
        display: flex;
        margin-bottom: 15px;
      }
      .chat-message .message-bubble {
        max-width: 60%;
        padding: 10px 15px;
        border-radius: 15px;
        font-size: 0.9em;
        line-height: 1.4;
        word-wrap: break-word;
      }
      .chat-message.bot .message-bubble {
        background-color: #e3f2fd;
        color: #333;
        margin-right: auto;
      }
      .chat-message.user .message-bubble {
        background-color: #0056b3;
        color: white;
        margin-left: auto;
      }
      .footer {
        background: #eaf3ff;
        text-align: center;
        padding: 10px;
        font-size: 0.8em;
        color: #666;
        border-top: 1px solid #ddd;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <!-- Header -->
      <div class="header">
        <h1>Chat Logs from Your AI Chatbot</h1>
      </div>

      <!-- Details Section -->
      <div class="details">
        <p><strong>Company Name:</strong> {{ company_name }}</p>
        <p><strong>Chatbot Name:</strong> {{ chatbot_name }}</p>
        <p><strong>Session ID:</strong> {{ session_id }}</p>
        <p><strong>IP Address:</strong> {{ ip_address }}</p>
        <p>
          <strong>Deployed URL:</strong>
          <a href="{{ base_link }}" target="_blank">{{ base_link }}</a>
        </p>
      </div>

      <!-- Chat Log -->
      <div class="chat-log">
        {% for message in chat_history %}
        <div class="chat-message {% if message.id == 'bot' %} bot {% else %} user {% endif %}">
          <div class="message-bubble">
            <div class="markdown-rendered" id="msg-{{ loop.index }}"></div>
          </div>
        </div>
        {% endfor %}
      </div>

      <!-- Footer -->
      <div class="footer">
        <p>Thank you for using our AI chatbot service!</p>
      </div>
    </div>

    <script>
      // Render Markdown messages
      document.addEventListener("DOMContentLoaded", () => {
        {% for message in chat_history %}
        const messageElement = document.getElementById("msg-{{ loop.index }}");
        messageElement.innerHTML = marked.parse(`{{ message.message }}`);
        {% endfor %}
      });
    </script>
  </body>
</html>

"""