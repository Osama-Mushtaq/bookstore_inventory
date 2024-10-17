# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate, UserInDB, UserBase
from app.database.connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
# Remove OAuth2PasswordBearer since we're using HTTPBearer
security = HTTPBearer()

@router.post("/register", response_model=UserBase, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    result = await db["users"].insert_one(user_dict)
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    return UserBase(**created_user)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    user = await db["users"].find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Import HTTPException and status at the top if not already imported
# from fastapi import HTTPException, status

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    token = credentials.credentials
    # Define the exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Use the token to decode and retrieve the user
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data = await db["users"].find_one({"username": username})
    if user_data is None:
        raise credentials_exception
    return UserInDB(**user_data)
