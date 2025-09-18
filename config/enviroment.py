from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_uri: str | None = None
    secret_key: str | None = None
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
