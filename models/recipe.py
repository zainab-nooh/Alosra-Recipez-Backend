from sqlalchemy import Column , Integer, String, ForeignKey, DateTime, Text, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from .base import BaseModel
from .user import UserModel


class Recipe(BaseModel):
    __tablename__ = "recipes"

    id = Column(Integer ,primary_key=True, index=True) 
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False ,index = True)
    base_price = Column(DECIMAL(10,2), nullable= False, index=True)
    prep_time_minutes = Column(Integer)
    difficulty = Column(String(20), default="medium") # optios easy-medium-hard
    image_url = Column(String(500))
    is_available= Column(Boolean, default=True, index=True)
    


    # Relationships
    category = relationship("Category", back_populates="recipes")
    order_items = relationship("OrderItem", back_populates='recipe')
    cart_items = relationship("CartItem", back_populates="recipe")


    
