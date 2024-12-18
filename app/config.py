from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "fastapi_db"
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    email_from: str = "noreply@example.com"
    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    smtp_user: str = "smtp_user"
    smtp_password: str = "smtp_password"
    
    class Config:
        env_file = ".env"

    
settings = Settings()