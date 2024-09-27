bot_chat_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Logs from Your AI Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
        }
        .details {
            margin-bottom: 20px;
        }
        .chat-log {
            background-color: #e9f7ef;
            border: 1px solid #c3e6cb;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        footer {
            margin-top: 20px;
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chat Logs from Your AI Chatbot</h1>

        <div class="details">
            <p><strong>Company Name:</strong> {{ company_name }}</p>
            <p><strong>Chatbot Name:</strong> {{ chatbot_name }}</p>
            <p><strong>Session ID:</strong> {{ session_id }}</p>
             <p><strong>IP Address:</strong> {{ ip_address }}</p>
            <p><strong>Deployed URL:</strong> {{ base_link }}</p>
        </div>

        <h2>Chat Log</h2>
        <div class="chat-log">
            <pre>{{ chat_history }}</pre>
        </div>
        
        <footer>
            <p>Thank you for using our AI chatbot service!</p>
        </footer>
    </div>
</body>
</html>
"""