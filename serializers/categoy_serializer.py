from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime 

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: str

    class Config:
        orm_mode = True

class CategoryResponseSchema(BaseModel):
    id: int
    is_active: bool
    display_order: int 
    created_at: datetime


    class Config: 
        orm_mode = True


class CategoryWithRecipes(CategoryResponseSchema):
    recipes: List["RecipeResponseSchema"] = []


from .recipe_serializers import RecipeResponseSchema
CategoryWithRecipes.model_rebuild()