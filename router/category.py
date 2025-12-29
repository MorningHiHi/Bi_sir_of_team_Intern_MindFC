from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from db.database import get_db
from controller import category
from schemas.user_schema import LoginResponse,LoginRequest,UserBase,UpdateUser
from typing import List
from setting import utils
from schemas.category_schema import IDN,CreateIDN,IdIDN


router = APIRouter(prefix="/category",tags=["Category"])

@router.post("/create_category")
def create_cate(data:CreateIDN,current_user=Depends(utils.get_current_user)):
    return category.create_category(data,current_user)

@router.get("")
def get_list_category(data=Depends(category.get_list_Category)):
    return data

@router.put("/updateCategory",response_model=IDN)
def updateCategory(data:IDN ,current_user = Depends(utils.get_current_user)):
    return category.put_update_Category(data,curent_user=current_user)

@router.delete("/deleteCategory")
def deleteCategory(text:IdIDN, current_user = Depends(category.get_current_user)):
    return category.del_delete_category(text,curent_user=current_user)

@router.get("/get_category_byId",response_model=IDN)
def get_category_byId(data:str,current_user=Depends(utils.get_current_user)):
    return category.categoryById(data,current_user)