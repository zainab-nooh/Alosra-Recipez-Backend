from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_uri: str
    secret_key: str
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
