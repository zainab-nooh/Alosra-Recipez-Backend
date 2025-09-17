from pydantic import BaseModel, field_validator
from typing import List, Optional
from decimal import Decimal
from enum import Enum
from datetime import datetime


# Order Status
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Schema for creating order items
class OrderItemCreate(BaseModel):
    recipe_id: int
    number_of_people: int

    @field_validator("number_of_people")
    @classmethod
    def validate_people_count(cls, v):
        if v < 1 or v > 20:
            raise ValueError("Number of People must be between 1 and 20")
        return v
    

# Schema for creating order 
class OrderCreate(BaseModel):
    delivery_address: str
    delivery_phone: str
    specila_notes: Optional[str] = None
    items: List[OrderItemCreate]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError("Order must contain at least 1 item")
        return v
    

#  Response Schema for Order items
class OrderItemResponseSchema(BaseModel):
    id: int
    recipe_id: int
    number_of_people: int
    unit_price: Decimal
    calculated_price: Decimal
    recipe: "RecipeResponseSchema"

    class Config:
        orm_mode = True


# Response Schema for orders
class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: OrderStatus
    delivery_address: str
    delivery_phone: str
    special_notes: Optional[str] = None 
    order_date: datetime
    estimated_delivery: Optional[datetime]
    created_at: datetime
    order_items: List[OrderItemResponseSchema] = []


    class Config:
        orm_mode = True


# Schema for returning Summarized orders 
class OrderSummarySchema(BaseModel):
    id: int
    total_amount: Decimal
    status: OrderStatus
    order_date: datetime
    items_count: int 

    class Config: 
        orm_mode = True


from .recipe_serializers import RecipeResponseSchema
OrderItemResponseSchema.model_rebuild()               



                                                      