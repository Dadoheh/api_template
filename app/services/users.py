# services/users.py
from fastapi import HTTPException, status
from ..models.db_models import UserInDB
from ..database import get_database
from ..services.auth import get_password_hash

async def get_user_by_email(email: str):
    db = await get_database()
    return await db.users.find_one({"email": email})

async def create_user(user_data: dict):
    db = await get_database()
    user_data["hashed_password"] = await get_password_hash(user_data.pop("password"))
    await db.users.insert_one(user_data)
    user = await get_user_by_email(user_data["email"])
    return user

async def update_user(email: str, update_data: dict):
    db = await get_database()
    if len(update_data) < 1:
        return await get_user_by_email(email)
    
    result = await db.users.update_one(
        {"email": email}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await get_user_by_email(email)