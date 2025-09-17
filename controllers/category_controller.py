from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.category import Category
from serializers.category_serializers import CategoryResponseSchema, CategoryWithRecipes

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryResponseSchema])
def get_all_categories(db: Session = Depends(get_db)):
    """Get all active categories ordered by display_order"""
    
    categories = db.query(Category).filter(
        Category.is_active == True
    ).order_by(Category.display_order.asc()).all()
    
    return [CategoryResponseSchema.model_validate(category) for category in categories]

@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """Get specific category by ID"""
    
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return CategoryResponseSchema.model_validate(category)

@router.get("/{category_id}/recipes", response_model=List[dict])
def get_recipes_by_category(category_id: int, db: Session = Depends(get_db)):
    """Get all available recipes in a specific category"""
    
    # First check if category exists
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Get recipes with category information
    from models.recipe import Recipe
    from serializers.recipe_serializers import RecipeResponseSchema
    
    recipes = db.query(Recipe).filter(
        Recipe.category_id == category_id,
        Recipe.is_available == True
    ).order_by(Recipe.name.asc()).all()
    
    # Convert to response format with category info
    recipe_responses = []
    for recipe in recipes:
        recipe_dict = RecipeResponseSchema.model_validate(recipe).model_dump()
        recipe_dict['category'] = CategoryResponseSchema.model_validate(category).model_dump()
        recipe_responses.append(recipe_dict)
    
    return recipe_responses