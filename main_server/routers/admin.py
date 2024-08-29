from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Annotated
from routers.auth import get_current_user
from models.tables import Chatbot_stats, Company,Queries,Users

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get("/total-stats")
async def get_total_stats(db:db_dependency,user: user_dependency):
    try:
        total_input_tokens = db.query(func.sum(Company.input_tokens)).scalar() or 0
        total_output_tokens = db.query(func.sum(Company.output_tokens)).scalar() or 0
        total_queries = db.query(func.count(Queries.id)).scalar() or 0
        print(type(total_queries),total_input_tokens,total_output_tokens)
        dollar_spend_input = (total_input_tokens)* (0.35/1000000)
        dollar_spend_output = (total_output_tokens) * (0.40/1000000)
        total_dollar_spend = (dollar_spend_input + dollar_spend_output)

        return JSONResponse(content={
            "input_tokens":total_input_tokens,
            "output_tokens":total_output_tokens,
            "requests":total_queries,
            "dollar_spend_input":dollar_spend_input,
            "dollar_spend_output":dollar_spend_output,
            "dollar_spend_total":total_dollar_spend
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Something went wrong not able to get the total stats")
    
@router.get("/companies")
async def all_companies(db:db_dependency,user: user_dependency):
    try:
        companies = db.query(Company).all()
        return JSONResponse(content={
            "companies":companies
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Unable to fetch all companies")
    


    







