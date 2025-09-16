from sqlalchemy import Column , Integer, String, ForeignKey,  DECIMAL, Text, DateTime, func
from sqlalchemy.orm import relationship
from .base import BaseModel


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    totoal_amount = Column(DECIMAL(10,2),nullable=False)
    status = Column(String(20), default="pending", index=True) # Options are pending, confirmed, preparing, out-for-delivery, delivered, cancelled
    delivery_address = Column(Text, nullable=False)
    delivery_phone = Column(String(20))
    special_notes = Column(Text)
    order_date = Column(DateTime(timezone=True), server_default=func.now(), index=True )
    estimated_delivery= Column(DateTime(timezone=True))


    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all,delete-orphan")



class OredrItem(BaseModel):
    __tablename = "order_items"

    id = Column(Integer , primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False, index=True)
    number_of_people = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(10,2), nullable=False) 
    calculated_price = Column(DECIMAL(10,2), nullable=False)


    # Relationships 
    order = relationship("Order", back_populates="order_items")
    recipe = relationship("Recipe", back_populates="order_items")
    
      