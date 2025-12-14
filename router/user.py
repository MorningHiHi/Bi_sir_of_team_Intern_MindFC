from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from db.database import get_db
from controller import user
from schemas.user_schema import LoginResponse,LoginRequest,UserBase
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
def get_list_user(data=Depends(user.get_list_user)):
    return data


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return user.login_user(data, db)

@router.post("/", response_model=UserBase)
def create_user(data: UserBase, db: Session = Depends(get_db)):
    return user.create_new_admin(data, db)


