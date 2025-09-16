from pydantic import BaseModel
from typing import Optional 
from datetime import datetime


# User Registartion/Creation
class UserScheme(BaseModel):
    name: str # User's Full anme
    email: str #User's email
    password: str
    country_code: Optional[str] = "+973"
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True 


# Returning User Data
class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    country_code: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None 
    is_active: bool


    class Config:
        orm_mode = True



# User Update 
         
class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    country_code: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True 

# User Login
class Userlogin(BaseModel):
    email: str
    password: str


# Rspone to user containing JWT
class UserToken(BaseModel):
    token: str
    message: str
    user: UserResponseSchema


    class Config:
        orm_mode = True