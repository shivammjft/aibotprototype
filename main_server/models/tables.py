from config.db import Base 
from datetime import datetime
from sqlalchemy import Integer, Column, Boolean, String , DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True) 
    username = Column(String(255), unique=True)  
    first_name = Column(String(50))  
    last_name = Column(String(50))  
    hashed_password = Column(String(255))  
    is_active = Column(Boolean, default=True)
    role = Column(String(50))


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True) 
    company_name = Column(String(255))
    company_key = Column(String(255))
    base_url = Column(String(255), unique=True) 
    input_tokens = Column(Integer)  
    output_tokens = Column(Integer)
    created_date = Column(DateTime, default=datetime.now())



class Chatbot_stats(Base):
    __tablename__ = "chatbots"

    id = Column(Integer,index=True)
    chatbot_id = Column(String(255),primary_key=True)
    chatbot_name  = Column(String(255))
    chatbot_prompt = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.id"))
    origin_url = Column(String(255))
    company_name = Column(String(255))
    total_input_tokens = Column(Integer)
    total_output_tokens= Column(Integer)
    total_queries = Column(Integer) 
    last_query_time = Column(DateTime)



class Queries(Base):
    __tablename__ = "queries"

    id = Column(Integer,index=True,primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    chatbot_id = Column(String(255),ForeignKey("chatbots.chatbot_id"))
    session_id = Column(String(255))
    query_text_bot = Column(Text)
    query_text_user = Column(Text)
    query_context = Column(Text)
    input_tokens = Column(String(255))
    output_tokens = Column(String(255))
    query_time = Column(DateTime)
    origin_url = Column(String(255))

