html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Bot Setup</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 1.5em;
            color: #007BFF;
            margin-top: 0;
        }
        pre {
            background: #eee;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .code-snippet {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: monospace;
        }
        .footer {
            font-size: 0.875em;
            color: #555;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Bot Setup</h1>
        <p>Description: The AI model is trained. Now you can use the credentials to access your personal AI bot at the given link.</p>
        
        <p><strong>Id:</strong> {company_id}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Company Name:</strong> {company_name}</p>
        <p><strong>Base Url:</strong> {base_link}</p>

        <p>Copy the code snippet below and insert it into your website's footer or header before the closing &lt;/body&gt; tag without any modification.</p>

        <pre class="code-snippet">
&lt;script
  id="ai-jellyfishbot"
  src="https://aibotfiles.vercel.app/script.js"
  defer&gt;
  {company_id},{company_name},{chatbot_name}
&lt;/script&gt;
        </pre>

        <div class="footer">
            If you have any questions, feel free to contact us.
        </div>
    </div>
</body>
</html>
'''
