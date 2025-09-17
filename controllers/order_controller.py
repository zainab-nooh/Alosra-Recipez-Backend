from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from decimal import Decimal
from datetime import datetime, timedelta
from database import get_db
from models.order import Order, OrderItem
from models.cart import CartItem
from models.recipe import Recipe
from models.user import UserModel
from serializers.order_serializers import OrderCreate, OrderResponseSchema, OrderSummarySchema, OrderStatus
from dependencies.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new order from cart items or provided items"""
    
    total_amount = Decimal('0.00')
    order_items_data = []
    
    # Process each item in the order
    for item in order_data.items:
        # Get recipe and verify availability
        recipe = db.query(Recipe).filter(
            Recipe.id == item.recipe_id,
            Recipe.is_available == True
        ).first()
        
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recipe with id {item.recipe_id} not found or not available"
            )
        
        # Calculate prices
        unit_price = recipe.base_price
        calculated_price = unit_price * Decimal(item.number_of_people)
        total_amount += calculated_price
        
        order_items_data.append({
            'recipe_id': item.recipe_id,
            'number_of_people': item.number_of_people,
            'unit_price': unit_price,
            'calculated_price': calculated_price
        })
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        delivery_address=order_data.delivery_address,
        delivery_phone=order_data.delivery_phone,
        special_notes=order_data.special_notes,
        estimated_delivery=datetime.utcnow() + timedelta(hours=2)  # 2 hours from now
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Create order items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            **item_data
        )
        db.add(order_item)
    
    db.commit()
    
    # Clear user's cart after successful order
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    
    # Reload order with all relationships
    order_with_items = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.recipe).joinedload(Recipe.category)
    ).filter(Order.id == order.id).first()
    
    return OrderResponseSchema.model_validate(order_with_items)

@router.get("/", response_model=List[OrderSummarySchema])
def get_user_orders(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """Get current user's order history"""
    
    orders = db.query(Order).options(
        joinedload(Order.order_items)
    ).filter(
        Order.user_id == current_user.id
    ).order_by(
        Order.order_date.desc()
    ).offset(skip).limit(limit).all()
    
    # Convert to summary format
    order_summaries = []
    for order in orders:
        order_summaries.append(OrderSummarySchema(
            id=order.id,
            total_amount=order.total_amount,
            status=OrderStatus(order.status),
            order_date=order.order_date,
            items_count=len(order.order_items)
        ))
    
    return order_summaries

@router.get("/{order_id}", response_model=OrderResponseSchema)
def get_order_details(
    order_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific order"""
    
    order = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.recipe).joinedload(Recipe.category)
    ).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return OrderResponseSchema.model_validate(order)

@router.put("/{order_id}/status", response_model=OrderResponseSchema)
def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update order status (for admin or delivery updates)"""
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Only allow certain status transitions
    valid_transitions = {
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['preparing', 'cancelled'],
        'preparing': ['out_for_delivery'],
        'out_for_delivery': ['delivered'],
        'delivered': [],  # No transitions from delivered
        'cancelled': []   # No transitions from cancelled
    }
    
    if new_status.value not in valid_transitions.get(order.status, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change status from {order.status} to {new_status.value}"
        )
    
    order.status = new_status.value
    db.commit()
    
    # Reload with relationships
    order_with_items = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.recipe).joinedload(Recipe.category)
    ).filter(Order.id == order.id).first()
    
    return OrderResponseSchema.model_validate(order_with_items)