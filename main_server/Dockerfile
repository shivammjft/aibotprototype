# 
FROM python:3.9

# 
WORKDIR /app

COPY . /app



# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV MONGO_URI=mongodb+srv://jellyfish:jelly1234@cluster0.lrqlckt.mongodb.net/
ENV OPENAI_API_KEY=sk-proj-4KvmEIU2qTT9LCcG8VHFT3BlbkFJwz6Jum3cwZaGq4PxBXVG
ENV GROQ_API_KEY=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
ENV LANGCHAIN_API_KEY=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
ENV REDIS_URL=redis://localhost:6379/0
ENV PINECONE_API_KEY=3ba6e5b4-aa32-4821-8e0c-e75e6a0e8998
ENV SENDER="shivam.pandey@jellyfishtechnologies.com"
ENV PASSWORD="vaee agwd chbh mhzm"

CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "8000"]