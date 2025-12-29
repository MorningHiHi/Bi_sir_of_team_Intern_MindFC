"""phần này là DTO nhận dữ liệu gốc từ client và lưu trữ tạm, trước khi thực hiện các bước chuyển đổi"""
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

class UpdateUser(UserBase):
    id:str=None
    username:str ="admin"
    password : str = "admin"

class LoginRequest(BaseModel):
    username: str="admin"
    password: str="admin"

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    # token_type: str = "bearer"
