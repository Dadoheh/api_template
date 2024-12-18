# routers/users.py
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import SecurityScopes
from typing import List
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..services.users import create_user, get_user_by_email, update_user
from ..middleware.auth import check_roles

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_new_user(user_data: UserCreate, admin: dict = Security(check_roles, scopes=["admin"])):
    if await get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(user_data.dict())
    return user

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Security(check_roles)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Security(check_roles)
):
    updated_user = await update_user(
        current_user["email"],
        user_update.dict(exclude_unset=True)
    )
    return updated_user

@router.get("/{email}", response_model=UserResponse)
async def get_user(email: str, admin: dict = Security(check_roles, scopes=["admin"])):
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user