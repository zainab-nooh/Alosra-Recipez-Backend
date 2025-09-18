from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URI: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7 
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:8081 "
    ENVIRONMENT: str = "development"

    # Uvicorn settings
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
