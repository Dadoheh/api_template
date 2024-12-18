# services/prompts.py
from fastapi import HTTPException
from ..database import get_database
from ..models.db_models import PromptInDB

async def create_prompt(prompt_data: dict, user_email: str):
    db = await get_database()
    prompt_data["created_by"] = user_email
    await db.prompts.insert_one(prompt_data)
    return await db.prompts.find_one({"title": prompt_data["title"]})

async def get_prompt(title: str):
    db = await get_database()
    return await db.prompts.find_one({"title": title})

async def update_prompt(title: str, update_data: dict):
    db = await get_database()
    result = await db.prompts.update_one(
        {"title": title}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return await get_prompt(title)

async def list_prompts(tags: List[str] = None):
    db = await get_database()
    query = {"is_active": True}
    if tags:
        query["tags"] = {"$all": tags}
    cursor = db.prompts.find(query)
    return await cursor.to_list(length=None)