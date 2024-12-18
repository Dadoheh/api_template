# routers/prompts.py
from fastapi import APIRouter, Security, HTTPException
from typing import List, Optional
from ..schemas.prompt import PromptCreate, PromptUpdate, PromptResponse
from ..services.prompts import create_prompt, get_prompt, update_prompt, list_prompts
from ..middleware.auth import check_roles

router = APIRouter()

@router.post("/", response_model=PromptResponse)
async def create_new_prompt(
    prompt: PromptCreate, 
    user: dict = Security(check_roles, scopes=["admin", "editor"])
):
    return await create_prompt(prompt.dict(), user["email"])

@router.get("/", response_model=List[PromptResponse])
async def get_prompts(tags: Optional[List[str]] = None):
    return await list_prompts(tags)

@router.get("/{title}", response_model=PromptResponse)
async def get_prompt_by_title(title: str):
    prompt = await get_prompt(title)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.put("/{title}", response_model=PromptResponse)
async def update_prompt_by_title(
    title: str,
    prompt: PromptUpdate,
    user: dict = Security(check_roles, scopes=["admin", "editor"])
):
    return await update_prompt(title, prompt.dict(exclude_unset=True))