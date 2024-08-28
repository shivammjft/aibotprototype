from fastapi import APIRouter, Depends,status, HTTPException
from config.db import SesssionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


def get_db():
    db = SesssionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]




