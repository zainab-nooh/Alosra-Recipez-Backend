from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime


# Schema for Recipes 
class RecipeBase(BaseModel):
    name: str
    description: str
    base_price: Decimal
    prep_time_minutes: Optional[int] = None
    difficulty: str = "medium" # options easy medium hard 
    image_url: Optional[str] = None


    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        if v not in ["easy", "medium", "hard"]:
            raise ValueError("Difficulty must be easy, medium, or hard")
        return v

    @field_validator("base_price")
    @classmethod
    def validate_base_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Base price must be greater than 0")
        return v


# Response Schema
class RecipeResponseSchema(RecipeBase):
    id: int
    category_id: int
    is_available: bool
    created_at: datetime
    category: Optional["CategoryResponseSchema"] = None

    class Config:
        from_attributes = True

# Extended response schema with calculated price
class RecipeWithPricing(RecipeResponseSchema):
    calculated_price: Optional[Decimal] = None

# Forward reference
from .category_serializers import CategoryResponseSchema
RecipeResponseSchema.model_rebuild()
