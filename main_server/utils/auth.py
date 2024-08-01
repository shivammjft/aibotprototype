from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from config.db import collection
from typing import Optional


def get_user_from_token(token: str) -> dict:
    user = collection.find_one({"company_id": token})
    if token: 
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token_type, token = auth_header.split()
    if token_type.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token type")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    user = get_user_from_token(token)
    return user