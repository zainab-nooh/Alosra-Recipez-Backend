from sqlalchemy import Column , Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel
from .user import UserModel


class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=True)
    description = Column(Text)
    image_url = Column(String(500))
    is_active = Column(Boolean ,fefault=True, inodex=True)
    display_order = Column(Integer, default=0, index=True)
    

    # RelationShips
    recipes = relationship("Recipe", back_populates="category", cascade="all.delete-orphan")
