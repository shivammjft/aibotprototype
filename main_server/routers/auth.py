from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from pydantic import BaseModel, field_validator
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import re 
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from models.tables import Users
from config.db import SessionLocal
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

crypt = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = "78f711bf23aeb4abee4bdd0bd01c8c431879c53b9a8466cd36cc43f1f0aacc52"
ALGORITHM = "HS256"

class Token(BaseModel):
    acess_token :str 
    token_type: str 

class UserBase(BaseModel):
    username: str
    email :str
    first_name: str 
    last_name: str 
    password: str
    role:str

    # @field_validator('password')
    # def validate_password(cls, v):
    #     if len(v) < 8:
    #         raise ValueError('Password must be at least 8 characters long.')
    #     if not re.search(r'[A-Z]', v):
    #         raise ValueError('Password must contain at least one uppercase letter.')
    #     if not re.search(r'[a-z]', v):
    #         raise ValueError('Password must contain at least one lowercase letter.')
    #     if not re.search(r'[0-9]', v):
    #         raise ValueError('Password must contain at least one numeric digit.')
    #     if not re.search(r'[\W_]', v):  
    #         raise ValueError('Password must contain at least one special character.')
    #     return v

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False 
    if not crypt.verify(password, user.hashed_password):
        return False 
    return user

def create_access_token(username:str, user_id:int, role:str, expire_delta:timedelta):
    encode = {"sub":username, 'id':user_id,'user_role':role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="could not verify user.")
        return {"username": username, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="could not verify user")
    

@router.post('/signup',status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency,
                 user:UserBase):
    
    create_user_model = Users(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        hashed_password = crypt.hash(user.password),
        role = user.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()


@router.post('/login')
async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
                db: db_dependency):
    user =authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="could not verify user.")
    token = create_access_token(user.username, user.role, user.id,timedelta(days=30))
    return {"access_token":token,'token_type':'bearer'}
