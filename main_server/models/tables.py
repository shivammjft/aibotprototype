from config.db import Base 
from sqlalchemy import Integer, Column, Boolean, String

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