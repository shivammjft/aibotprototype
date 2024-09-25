from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from models.tables import Company
from config.db import SessionLocal
from sqlalchemy.orm import Session
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    logger.info("Received request: %s", request.url)
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        logger.warning("Authorization header missing")
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token_type, token = auth_header.split()
    except ValueError:
        logger.error("Invalid Authorization header format: %s", auth_header)
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    if token_type.lower() != "bearer":
        logger.warning("Invalid token type: %s", token_type)
        raise HTTPException(status_code=401, detail="Invalid token type")
    

    origin_header = request.headers.get("Origin")
    if not origin_header:
        logger.warning("Origin header missing")
        raise HTTPException(status_code=403, detail="Origin header missing")

    if not token:
        logger.warning("Token missing in Authorization header")
        raise HTTPException(status_code=401, detail="Token missing")


    logger.info("Validating token: %s", token)

    user = get_user_from_api_key(token, db)
    
    if not user:
        logger.warning("User not found for token: %s", token)
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info("User successfully retrieved: %s")  
    return user
