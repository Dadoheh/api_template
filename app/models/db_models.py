# app/models/db_models.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserInDB(BaseModel):
    email: EmailStr
    username: str 
    hashed_password: str
    roles: List[str] = ["user"]
    is_active: bool = True
    created_at: datetime = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe", 
                "roles": ["user"],
                "is_active": True
            }
        }
        
        
class PromptInDB(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    created_by: EmailStr
    created_at: datetime = datetime.now()
    is_active: bool = True
    


class EmailTemplateInDB(BaseModel):
    name: str
    subject: str
    body: str
    variables: List[str] = []
    created_by: EmailStr
    created_at: datetime = datetime.now()
    is_active: bool = True