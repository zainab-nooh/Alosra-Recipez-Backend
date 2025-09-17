from sqlalchemy import Column , Integer, String, ForeignKey,  DECIMAL, Text, DateTime, UniqueConstraint 
from sqlalchemy.orm import relationship
from .base import BaseModel


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False, index=True)
    number_of_people = Column(Integer, nullable=False, default=1)


    # Relationships

    user = relationship("UserModel", back_populates="cart_items")
    recipe = relationship("Recipe", back_populates="cart_items")


    # CONSTRAINTS
    __table_args__ = (UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_cart'),)