from pydantic import BaseModel,Field,EmailStr,HttpUrl
from typing import List , Dict,Optional, Any
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
    base_url : Optional[HttpUrl]
    email:str =EmailStr
    deployment_url:Optional[HttpUrl]  
    chatbot_name: str = Field(min_length=1, max_length=100)



class AddDataRequest(BaseModel):
    text: str           
    source: str         
    title: str          
    description: str  
    collection_name: str 

class DeleteDataRequest(BaseModel):
    document_id: List[str]
    collection_name: str

class SearchDataByMetaDataRequest(BaseModel):
    key: str
    value: str
    collection_name: str
    to_retrive: Optional[int] = 100

class DocumentResponse(BaseModel):
    id: str
    content: str
    metadata: dict

class UpdatePromptRequest(BaseModel):
    chatbot_prompt: str


class SendChat(BaseModel):
    chatHistory:List
    chatbot_id:str
    session_id:str


class AddVisitorRequest(BaseModel):
    origin_url: Optional[str]
    session_id: Optional[str]
    chatbot_id: Optional[str]
    timezone: Optional[str] = None  
    language: Optional[str] = None 
    is_mobile: Optional[bool] = Field(None, alias="isMobile") 
    user_agent: Optional[str] = Field(None, alias="userAgent")  
    platform: Optional[str] = None  
    referrer: Optional[str] = None  
    location: Optional[Any] = None  
    network_type: Optional[str] = Field(None, alias="networkType")  
    email:Optional[str] = None
    phone_number:Optional[str] =  Field(None, alias="phoneNumber")
 



class QueryUserResponse(BaseModel):
    id: int
    session_id: str
    ip_address: str 
    origin_url: str
    timezone: Optional[str] = None  
    language: Optional[str] = None  
    is_mobile: Optional[bool] = None 
    user_agent: Optional[str] = None  
    platform:Optional[str] = None  
    referrer: Optional[str] = None  
    location:Optional[Any] = None  
    network_type: Optional[str] = None  
