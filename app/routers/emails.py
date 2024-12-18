# routers/emails.py
from fastapi import APIRouter, Security, HTTPException
from typing import List
from ..schemas.email import (
    EmailTemplateCreate, 
    EmailTemplateUpdate,
    EmailTemplateResponse,
    EmailSend
)
from ..services.emails import (
    create_template,
    get_template, 
    update_template,
    list_templates,
    send_email
)
from ..middleware.auth import check_roles

router = APIRouter()

@router.post("/templates/", response_model=EmailTemplateResponse)
async def create_email_template(
    template: EmailTemplateCreate,
    user: dict = Security(check_roles, scopes=["admin"])
):
    return await create_template(template.dict(), user["email"])

@router.get("/templates/", response_model=List[EmailTemplateResponse])
async def get_templates():
    return await list_templates()

@router.get("/templates/{name}", response_model=EmailTemplateResponse)
async def get_template_by_name(name: str):
    template = await get_template(name)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put("/templates/{name}", response_model=EmailTemplateResponse)
async def update_template_by_name(
    name: str,
    template: EmailTemplateUpdate,
    user: dict = Security(check_roles, scopes=["admin"])
):
    return await update_template(name, template.dict(exclude_unset=True))

@router.post("/send")
async def send_template_email(
    email_data: EmailSend,
    user: dict = Security(check_roles)
):
    await send_email(
        email_data.template_name,
        email_data.to_email,
        email_data.variables
    )
    return {"status": "Email sent successfully"}