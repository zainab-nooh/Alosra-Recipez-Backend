from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.enviroment import settings  
from models.base import Base


DB_URI = settings.DB_URI
SECRET_KEY = settings.SECRET_KEY




engine = create_engine(
    DB_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_tables():
    """Drop all database tables - USE WITH CAUTION"""
    print("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped!")

def reset_database():
    """Drop and recreate all tables - USE WITH CAUTION"""
    print("Resetting database...")
    drop_tables()
    create_tables()
    print("Database reset complete!")

if __name__ == "__main__":
    # This allows you to run: python database.py
    create_tables()