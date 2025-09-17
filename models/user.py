from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt 
from config.enviroment import settings 


# Creating a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email= Column(String, unique=True)
    password_hash = Column(String, nullable=True) 
    country_code = Column(String(10), default="+973")   
    phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True, index=True) 

    # NEW: Relationship - a user can have multiple cart_items
    orders = relationship("Order", back_populates="user", cascade="all,delete-orphan")
    
    cart_items = relationship('CartItem', back_populates='user', cascade="all,delete-orphan")

# Method to set a password 
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)


# Method to verify a password 
    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)
    


    def generate_token(self):
        # Define the payload 
        payload = {
            "exp": datetime.now(timezone.utc) +  timedelta(days=1),
            "iat": datetime.now(timezone.utc), 
            "sub": str(self.id),
        }

        # create JWT Token 
        token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
        return token
    