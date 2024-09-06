from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from typing import Annotated,Dict
from routers.auth import get_current_user,get_current_user_with_token
from models.tables import Chatbot_stats, Company,Queries,Users
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import HttpUrl
import os



router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


INPUT_TOKEN_RATE = 0.35 / 1_000_000
OUTPUT_TOKEN_RATE = 0.40 / 1_000_000

def company_to_dict(company) -> Dict:
    input_token_cost = company.input_tokens * INPUT_TOKEN_RATE
    output_token_cost = company.output_tokens * OUTPUT_TOKEN_RATE


    return {
        "id": company.id,
        "company_key": company.company_key,
        "input_tokens": company.input_tokens,
        "created_date": company.created_date.isoformat(), 
        "company_name": company.company_name,
        "base_url": company.base_url,
        "email": company.email,
        "output_tokens": company.output_tokens,
        "input_token_cost": input_token_cost,  
        "output_token_cost": output_token_cost
    }


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user_with_token)]


@router.get("/total-stats")
async def get_total_stats(db:db_dependency,user: user_dependency):
    try:
        total_input_tokens = db.query(func.sum(Company.input_tokens)).scalar() or 0
        total_output_tokens = db.query(func.sum(Company.output_tokens)).scalar() or 0
        total_queries = db.query(func.count(Queries.id)).scalar() or 0
        
        total_input_tokens = Decimal(total_input_tokens)
        total_output_tokens = Decimal(total_output_tokens)
        
        
        input_rate = Decimal('0.35') / Decimal('1000000')
        output_rate = Decimal('0.40') / Decimal('1000000')
        
        
        dollar_spend_input = total_input_tokens * input_rate
        dollar_spend_output = total_output_tokens * output_rate
        total_dollar_spend = dollar_spend_input + dollar_spend_output

        return JSONResponse(content={
            "status":"200",
            "data":{
            "input_tokens":float(total_input_tokens),
            "output_tokens":float(total_output_tokens),
            "requests":total_queries,
            "dollar_spend_input":float(dollar_spend_input),
            "dollar_spend_output":float(dollar_spend_output),
            "dollar_spend_total":float(total_dollar_spend)}
        })
    except Exception as e:
        print(e)
        return JSONResponse(content="Something went wrong not able to get the total stats")
    
@router.get("/companies",status_code=status.HTTP_200_OK)
async def all_companies(db:db_dependency,user: user_dependency):
    try:
        companies = db.query(Company).all()

        companies_list = [company_to_dict(company) for company in companies]
        return JSONResponse(
            content={
                "status": status.HTTP_200_OK,
                "data": companies_list
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail="Unable to fetch all companies")
    



@router.post("/upload/")
async def upload_files(company_name:str,base_url:HttpUrl ,files: list[UploadFile] = File(...)):
    
    folder_name = f"{company_name}-{base_url}"
    dir_path = os.path.join("uploads", folder_name)
    
    os.makedirs(dir_path, exist_ok=True)

    file_paths = []
    for file in files:
        file_path = os.path.join(dir_path, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        file_paths.append(file_path)

    return JSONResponse(content={"file_paths": file_paths}, status_code=200)




    







