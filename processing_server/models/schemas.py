from pydantic import BaseModel

class LinkRequest(BaseModel):
    url: str