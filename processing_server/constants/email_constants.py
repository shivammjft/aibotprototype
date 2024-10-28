bot_ready_email_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Model Credentials</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
        }
        .code-snippet {
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <p>The AI model is trained. Now you can use the credentials to access your personal AI bot.</p>
        
        <p><strong>API_KEY:</strong> {{ company_id }}<br>
        <strong>Company Name:</strong> {{ company_name }}<br>
        <strong>Base Url:</strong> {{ base_link }}</p>

        <p>Copy the code snippet below and insert it into your website's footer or header before the closing &lt;/body&gt; tag without any modification:</p>
        
        <div class="code-snippet">
            &lt;script<br>
            id="ai-jellyfishbot"<br>
            src="https://aibotfiles.vercel.app/script.js"<br>
            defer&gt;<br>
            data-api-key="{{ API_KEY }}"
            data-bot-id="{{ CHATBOT_KEY }}"
            data-company-name="{{ company_name }}"
            data-bot-name="{{ chatbot_name }}"
            <br>
            &lt;/script&gt;
        </div>
    </div>
</body>
</html>
"""