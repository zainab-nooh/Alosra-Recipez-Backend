from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"
    
    # Remove duplicate id - it's inherited from BaseModel
    name = Column(String(100), unique=True, nullable=False)  # Changed to nullable=False
    description = Column(Text)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True, index=True)  # FIXED typos
    display_order = Column(Integer, default=0, index=True)
    
    # Relationships - FIXED cascade syntax
    recipes = relationship("Recipe", back_populates="category", cascade="all,delete-orphan")
