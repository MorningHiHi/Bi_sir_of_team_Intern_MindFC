from pydantic import BaseModel
from typing import Optional
from .general import ListGeneral,ID_NAME
class UserBase(BaseModel):
    username: str="admin"
    # email: str="admin@gmail.com"
    password:str="admin"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

class LoginRequest(BaseModel):
    username: str="admin"
    password: str="admin"

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    # token_type: str = "bearer"
