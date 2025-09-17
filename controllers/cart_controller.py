from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List
from decimal import Decimal
from database import get_db
from models.cart import CartItem
from models.recipe import Recipe
from models.user import UserModel
from serializers.cart_serializers import CartItemCreate, CartItemUpdate, CartItemResponseSchema, CartResponseSchema
from dependencies.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

def _create_cart_item_response(cart_item: CartItem) -> CartItemResponseSchema:
    """Helper function to create cart item response with calculated price"""
    calculated_price = cart_item.recipe.base_price * Decimal(cart_item.number_of_people)
    
    # Create response and set calculated price
    response = CartItemResponseSchema.model_validate(cart_item)
    response.calculated_price = calculated_price
    
    return response

@router.get("/", response_model=CartResponseSchema)
def get_user_cart(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's cart items"""
    
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.recipe).joinedload(Recipe.category)
    ).filter(CartItem.user_id == current_user.id).all()
    
    # Calculate totals and prepare response
    total_amount = Decimal('0.00')
    cart_item_responses = []
    
    for cart_item in cart_items:
        cart_response = _create_cart_item_response(cart_item)
        total_amount += cart_response.calculated_price
        cart_item_responses.append(cart_response)
    
    return CartResponseSchema(
        items=cart_item_responses,
        total_amount=total_amount,
        total_items=len(cart_item_responses)
    )

@router.post("/add", response_model=CartItemResponseSchema)
def add_item_to_cart(
    cart_item_data: CartItemCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add recipe to cart or update quantity if already exists"""
    
    # Check if recipe exists and is available
    recipe = db.query(Recipe).filter(
        Recipe.id == cart_item_data.recipe_id,
        Recipe.is_available == True
    ).first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found or not available"
        )
    
    # Check if item already exists in cart
    existing_cart_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.recipe_id == cart_item_data.recipe_id
    ).first()
    
    if existing_cart_item:
        # Update existing item
        existing_cart_item.number_of_people = cart_item_data.number_of_people
        db.commit()
        cart_item = existing_cart_item
    else:
        # Create new cart item
        cart_item = CartItem(
            user_id=current_user.id,
            recipe_id=cart_item_data.recipe_id,
            number_of_people=cart_item_data.number_of_people
        )
        
        db.add(cart_item)
        try:
            db.commit()
            db.refresh(cart_item)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error adding item to cart"
            )
    
    # Load with relationships for response
    cart_item_with_recipe = db.query(CartItem).options(
        joinedload(CartItem.recipe).joinedload(Recipe.category)
    ).filter(CartItem.id == cart_item.id).first()
    
    return _create_cart_item_response(cart_item_with_recipe)

@router.put("/item/{cart_item_id}", response_model=CartItemResponseSchema)
def update_cart_item(
    cart_item_id: int,
    cart_item_update: CartItemUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    
    cart_item = db.query(CartItem).options(
        joinedload(CartItem.recipe).joinedload(Recipe.category)
    ).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Update the item
    cart_item.number_of_people = cart_item_update.number_of_people
    db.commit()
    db.refresh(cart_item)
    
    return _create_cart_item_response(cart_item)

@router.delete("/item/{cart_item_id}")
def remove_cart_item(
    cart_item_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart successfully"}

@router.delete("/clear")
def clear_cart(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all items from user's cart"""
    
    deleted_count = db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": f"Cart cleared successfully. {deleted_count} items removed."}