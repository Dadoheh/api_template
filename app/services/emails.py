# services/emails.py
from fastapi import HTTPException
from ..database import get_database
import emails
from ..config import settings
from ..models.db_models import EmailTemplateInDB

async def create_template(template_data: dict, user_email: str):
    db = await get_database()
    template_data["created_by"] = user_email
    await db.email_templates.insert_one(template_data)
    return await db.email_templates.find_one({"name": template_data["name"]})

async def get_template(name: str):
    db = await get_database()
    return await db.email_templates.find_one({"name": name})

async def update_template(name: str, update_data: dict):
    db = await get_database()
    result = await db.email_templates.update_one(
        {"name": name}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Template not found")
    return await get_template(name)

async def list_templates():
    db = await get_database()
    cursor = db.email_templates.find({"is_active": True})
    return await cursor.to_list(length=None)

async def send_email(template_name: str, to_email: str, variables: dict):
    template = await get_template(template_name)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    try:
        subject = template["subject"].format(**variables)
        body = template["body"].format(**variables)
        
        message = emails.Message(
            subject=subject,
            html=body,
            mail_from=settings.email_from
        )
        
        r = message.send(
            to=to_email,
            smtp={
                "host": settings.smtp_host,
                "port": settings.smtp_port,
                "user": settings.smtp_user,
                "password": settings.smtp_password,
                "tls": True
            }
        )
        
        if not r.status_code == 250:
            raise HTTPException(status_code=500, detail="Failed to send email")
            
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required variable: {str(e)}"
        )