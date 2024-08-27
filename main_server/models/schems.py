from pydantic import BaseModel
from typing import List , Dict,Optional
from datetime import datetime



class RequestModel(BaseModel):
    query: str
    context: Optional[list[str]] = None
    session_id: str

class Company(BaseModel):
    name: str
    metadata: dict


class ClientRequest(BaseModel):
    company_name : str
    base_link : str
    email:str
    deployment_link:str
    chatbot_name: str