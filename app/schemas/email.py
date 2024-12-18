# schemas/email.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body: str
    variables: List[str] = []

class EmailTemplateUpdate(BaseModel):
    subject: Optional[str]
    body: Optional[str]
    variables: Optional[List[str]]
    is_active: Optional[bool]

class EmailTemplateResponse(BaseModel):
    name: str
    subject: str
    body: str
    variables: List[str]
    created_by: EmailStr
    created_at: datetime
    is_active: bool

class EmailSend(BaseModel):
    template_name: str
    to_email: EmailStr
    variables: Dict[str, str]