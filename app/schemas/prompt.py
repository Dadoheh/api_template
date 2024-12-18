# schemas/prompt.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PromptCreate(BaseModel):
    title: str
    content: str 
    tags: List[str] = []

class PromptUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    is_active: Optional[bool]

class PromptResponse(BaseModel):
    title: str
    content: str
    tags: List[str]
    created_by: EmailStr
    created_at: datetime
    is_active: bool