# schemas/user.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    roles: List[str] = ["user"]

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    roles: Optional[List[str]]
    is_active: Optional[bool]

class UserResponse(BaseModel):
    email: EmailStr
    username: str
    roles: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "roles": ["user"],
                "is_active": True,
                "created_at": "2024-03-14T12:00:00"
            }
        }