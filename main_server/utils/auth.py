from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.tables import Company
from config.db import SessionLocal
from sqlalchemy.orm import Session



def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_user_from_api_key(api_key: str,db) -> dict:
    user  = db.query(Company).filter(Company.company_key == api_key).first() 
    return user



async def get_current_user(request: Request) -> dict:
    db = next(get_db())
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token_type, token = auth_header.split()
    if token_type.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    origin_header = request.headers.get("Origin")
    if not  origin_header:
        raise HTTPException(status_code=403, detail="Origin header missing")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    user = get_user_from_api_key(token,db)
    # if origin_header not in user["deploymnet_url"]:
    #     raise HTTPException(status_code=403, detail="Origin not allowed restricted")
    return user

