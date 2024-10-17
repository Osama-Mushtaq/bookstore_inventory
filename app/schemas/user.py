# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from .book import PyObjectId  # Import PyObjectId from book schema

class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: Optional[str] = None
    role: str = Field(default="user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
