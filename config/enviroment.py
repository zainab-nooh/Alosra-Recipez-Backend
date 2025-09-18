from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = False

    # Uvicorn settings
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
