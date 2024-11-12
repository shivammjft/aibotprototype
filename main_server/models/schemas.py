from pydantic import BaseModel,Field,EmailStr,HttpUrl
from typing import List , Dict,Optional
from datetime import datetime



class RequestModel(BaseModel):
    query: str
    context: Optional[list[dict]] = None
    session_id: str
    chatbot_id:str

class Company(BaseModel):
    name: str
    metadata: dict


class ClientRequest(BaseModel):
    company_name : str = Field(min_length=3, max_length=100)
    base_url : HttpUrl
    email:str =EmailStr
    deployment_url:Optional[HttpUrl]  
    chatbot_name: str = Field(min_length=1, max_length=100)

class AddDataRequest(BaseModel):
    text: str           
    source: str         
    title: str          
    description: str  
    collection_name: str 

class UpdatePromptRequest(BaseModel):
    chatbot_prompt: str


class SendChat(BaseModel):
    chatHistory:List
    chatbot_id:str
    session_id:str


class AddVisitorRequest(BaseModel):
    origin_url: str
    session_id: str
    country: str