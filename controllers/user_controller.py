from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.user import UserModel
from serializers.user_serializers import UserSchema, UserToken, UserLogin, UserResponseSchema, UserUpdateSchema
from database import get_db
from dependencies.auth import get_current_user
from config.enviroment import settings

router = APIRouter()


@router.post("/register", response_model=UserResponseSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.name == user.name) | (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = UserModel(name=user.name, email=user.email)
    # Use the set_password method to hash the password
    new_user.set_password(user.password)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find the user by email
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    # Check if the user exists and if the password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate JWT token
    token = db_user.generate_token()
    user_response = UserResponseSchema.from_orm(db_user)


    # Return token and a success message
    return {"token": token, "message": "Login successful", "user": user_response}

@router.get('/users', response_model=List[UserResponseSchema])
def get_users(db: Session=Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user





@router.get("/me", response_model=UserResponseSchema)
def get_current_user_profile(current_user: UserModel = Depends(get_current_user)):
    """Get current authenticated user's profile"""
    return current_user



@router.put("/profile", response_model=UserResponseSchema)
def update_user_profile(
    user_update: UserUpdateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.phone is not None:
        current_user.phone = user_update.phone
    if user_update.address is not None:
        current_user.address = user_update.address
    if user_update.country_code is not None:
        current_user.country_code = user_update.country_code

    db.commit()
    db.refresh(current_user)
    return current_user
