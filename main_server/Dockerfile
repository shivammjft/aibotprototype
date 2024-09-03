# 
FROM python:3.9

# 
WORKDIR /app

COPY . /app



# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV MYSQL_URI=mysql+pymysql://root:12345678@mysql:3306/chatbotserver
ENV OPENAI_API_KEY=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
ENV GROQ_API_KEY=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
ENV LANGCHAIN_API_KEY=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
ENV REDIS_URL=redis://redis_server:6379/0
ENV RABBITMQ_HOST="rabbitmq-server"
ENV QDRANT_URL="qDrant_server:6333"
CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "8000"]