from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.enviroment import settings  


DATABASE_URL = settings.db_uri
SECRET_KEY = settings.secret_key


engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
