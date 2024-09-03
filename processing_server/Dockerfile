# 
FROM python:3.9

# 
WORKDIR /app

COPY . /app


# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV MYSQL_URI=mysql+pymysql://root:12345678@mysql:3306/chatbotserver
ENV OPENAI_API_KEY=sk-proj-4KvmEIU2qTT9LCcG8VHFT3BlbkFJwz6Jum3cwZaGq4PxBXVG
ENV LANGCHAIN_API_KEY=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
ENV SENDER="shivam.pandey@jellyfishtechnologies.com"
ENV MAILJET_API_KEY=b206a37878213791ca36f654de1a5ee4
ENV MAILJET_SECRET_KEY=0186662647f8ca1a38953139ce28ff3a
ENV RABBITMQ_HOST="rabbitmq-server"
ENV QDRANT_URL="qDrant-server:6333"
CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "9000"]
