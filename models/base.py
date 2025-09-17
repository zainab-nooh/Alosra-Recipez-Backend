from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Added timezone
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Added timezone
