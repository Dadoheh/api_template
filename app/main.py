from fastapi import FastAPI
from .database import connect_to_mongo, close_mongo_connection
from .routers import auth, users, prompts, emails

app = FastAPI(title="FastAPI Project")

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
app.include_router(emails.router, prefix="/emails", tags=["emails"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Project"}