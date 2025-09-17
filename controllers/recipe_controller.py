from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from decimal import Decimal
from database import get_db
from models.recipe import Recipe
from models.category import Category
from serializers.recipe_serializers import RecipeResponseSchema, RecipeWithPricing

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/", response_model=List[RecipeResponseSchema])
def get_all_recipes(
    skip: int = Query(0, ge=0, description="Number of recipes to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of recipes to return"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    db: Session = Depends(get_db)
):
    """Get all available recipes with optional filtering"""
    
    query = db.query(Recipe).options(joinedload(Recipe.category)).filter(
        Recipe.is_available == True
    )
    
    # Apply filters
    if category_id:
        query = query.filter(Recipe.category_id == category_id)
    
    if difficulty:
        if difficulty not in ['easy', 'medium', 'hard']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Difficulty must be 'easy', 'medium', or 'hard'"
            )
        query = query.filter(Recipe.difficulty == difficulty)
    
    # Apply pagination and ordering
    recipes = query.order_by(Recipe.name.asc()).offset(skip).limit(limit).all()
    
    return [RecipeResponseSchema.model_validate(recipe) for recipe in recipes]

@router.get("/{recipe_id}", response_model=RecipeResponseSchema)
def get_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    """Get specific recipe with category information"""
    
    recipe = db.query(Recipe).options(joinedload(Recipe.category)).filter(
        Recipe.id == recipe_id,
        Recipe.is_available == True
    ).first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    return RecipeResponseSchema.model_validate(recipe)

@router.get("/{recipe_id}/pricing", response_model=RecipeWithPricing)
def get_recipe_with_pricing(
    recipe_id: int, 
    people: int = Query(1, ge=1, le=20, description="Number of people"),
    db: Session = Depends(get_db)
):
    """Get recipe with calculated pricing for specified number of people"""
    
    recipe = db.query(Recipe).options(joinedload(Recipe.category)).filter(
        Recipe.id == recipe_id,
        Recipe.is_available == True
    ).first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    # Calculate price for specified number of people
    calculated_price = recipe.base_price * Decimal(people)
    
    recipe_dict = RecipeResponseSchema.model_validate(recipe).dict()
    recipe_dict['calculated_price'] = calculated_price
    
    return RecipeWithPricing(**recipe_dict)