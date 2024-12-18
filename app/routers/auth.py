# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth import Token, UserAuth
from ..services.auth import create_access_token, verify_password, get_password_hash
from ..database import get_database

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_data: UserAuth):
    db = await get_database()
    if await db.users.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user_dict = user_data.dict()
    user_dict["hashed_password"] = await get_password_hash(user_dict.pop("password"))
    await db.users.insert_one(user_dict)
    
    access_token = await create_access_token({"sub": user_data.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = await get_database()
    user = await db.users.find_one({"email": form_data.username})
    if not user or not await verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}