# cart_serializers.py - FINAL FIXED VERSION
from pydantic import BaseModel, field_validator, computed_field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

# Base Schema for cart
class CartItemBase(BaseModel):
    recipe_id: int
    number_of_people: int
    
    @field_validator("number_of_people")
    @classmethod
    def validate_people_count(cls, v):
        if v < 1 or v > 20:
            raise ValueError("Number of people must be between 1 and 20")
        return v

# Schema for creating cart items
class CartItemCreate(CartItemBase):
    pass

# Schema for updating cart items
class CartItemUpdate(BaseModel):
    number_of_people: int

# Response Schema for cart items
class CartItemResponseSchema(CartItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    recipe: "RecipeResponseSchema"
    
    # Add calculated_price as an optional field that will be set manually
    calculated_price: Optional[Decimal] = None
    
    model_config = {"from_attributes": True}

# Response Schema for full cart
class CartResponseSchema(BaseModel):
    items: List[CartItemResponseSchema] = []
    total_amount: Decimal
    total_items: int

# Forward reference - keep at bottom
from .recipe_serializers import RecipeResponseSchema
CartItemResponseSchema.model_rebuild()