from fastapi import APIRouter, Depends, status, HTTPException, Request
from passlib.context import CryptContext
from pydantic import BaseModel, field_validator
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import re 
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from models.tables import Users
from config.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import logging
from models.tables import Company

router = APIRouter(prefix='/auth', tags=['Auth'])

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


crypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = "78f711bf23aeb4abee4bdd0bd01c8c431879c53b9a8466cd36cc43f1f0aacc52"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str 
    token_type: str 

class ValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class LoginUserData(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValidationException({"status": False, "mssg": 'Password must be at least 8 characters long.'})       
        if not re.search(r'[A-Z]', v):
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one uppercase letter.'})       
        if not re.search(r'[a-z]', v):
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one lowercase letter.'})
        if not re.search(r'[0-9]', v):
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one numeric digit.'})
        if not re.search(r'[\W_]', v):  
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one special character.'})
        return v

class UserBase(BaseModel):
    username: str
    email: str
    first_name: str 
    last_name: str 
    password: str
    role: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValidationException({"status": False, "mssg": 'Password must be at least 8 characters long.'})       
        if not re.search(r'[A-Z]', v):
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one uppercase letter.'})       
        if not re.search(r'[a-z]', v):
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one lowercase letter.'})
        if not re.search(r'[0-9]', v):
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one numeric digit.'})
        if not re.search(r'[\W_]', v):  
            raise ValidationException({"status": False, "mssg": 'Password must contain at least one special character.'})
        return v

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise ValidationException({"status": False, "mssg": 'Authorization Header missing.'})   
    token_type, token = auth_header.split()
    if token_type.lower() != "bearer":
        raise ValidationException({"status": False, "mssg": 'Token type is not bearer.'})   
    return token

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        logger.warning("Authentication failed: Username does not exist: %s", username)
        raise ValidationException({"status": False, "mssg": 'Username does not exist.'})       
    if not crypt.verify(password, user.hashed_password):
        logger.warning("Authentication failed: Incorrect password for user: %s", username)
        raise ValidationException({"status": False, "mssg": 'Password does not match.'})       
    logger.info("User authenticated successfully: %s", username)
    return user

def create_access_token(username: str, user_id: int, role: str, expire_delta: timedelta):
    encode = {"sub": username, 'id': user_id, 'user_role': role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user_with_token(token: Annotated[str, Depends(get_token)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            logger.error("Failed to verify user: username or user_id is None.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify user.")
        logger.info("Current user verified: %s", username)
        return {"username": username, 'id': user_id}
    except JWTError:
        logger.error("JWT error during user verification.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify user")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            logger.error("Failed to verify user: username or user_id is None.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify user.")
        logger.info("Current user verified: %s", username)
        return {"username": username, 'id': user_id}
    except JWTError:
        logger.error("JWT error during user verification.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify user")

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency, user: UserBase):
    existing_user = db.query(Users).filter((Users.username == user.username) | (Users.email == user.email)).first()

    if existing_user:
        if existing_user.username == user.username:
            logger.warning("Signup failed: Username already exists: %s", user.username)
            raise ValidationException({"status": False, "mssg": 'Username already exists.'})       

        if existing_user.email == user.email:
            logger.warning("Signup failed: User email already exists: %s", user.email)
            raise ValidationException({"status": False, "mssg": 'User email already exists.'})       

    create_user_model = Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=crypt.hash(user.password),
        role=user.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    logger.info("User account created successfully: %s", user.username)
    return JSONResponse(content={"detail": {"status": True, "mssg": "Account Created Successfully!"}})

user_dependency = Annotated[dict, Depends(get_current_user)]
@router.post('/login')
async def login(form_data: LoginUserData, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.username, user.id, user.role, timedelta(days=30))
    logger.info("User logged in successfully: %s", user.username)
    if  user.role =='admin':
        return JSONResponse(content={"access_token": token, 'token_type': 'bearer','role':user.role})
    else:
        company = db.query(Company).filter(Company.email == user.email).first()
        company_json = {
            "email": company.email,
            "company_name": company.company_name,
            "base_url": company.base_url,
            "company_id": company.company_key
        }
        return JSONResponse(content={"access_token": token, 'token_type': 'bearer','role':user.role,'company_data':company_json})
