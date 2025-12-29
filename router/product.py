from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from db.database import get_db
from controller import product
from schemas.product_schema import Product
from schemas.user_schema import LoginResponse,LoginRequest,UserBase,UpdateUser
from typing import List
from setting import utils

router = APIRouter(prefix="/products",tags=["Product"])

@router.get("")
def get_list_product(data=Depends(product.get_list_product)):
    return data

@router.post("/product",response_model=Product)
def create_NewProduct(data: Product,current_user = Depends(utils.get_current_user)):
    return product.create_product(data,current_user)


@router.put("/updateProduct",response_model=Product)
def updateUser(data:Product ,current_user = Depends(utils.get_current_user)):
    return product.put_update_product(data,current_user)


@router.delete("/deleteProduct")
def deleteUser(text:Product, current_user = Depends(utils.get_current_user)):
    return product.del_delete_product(text,curent_user=current_user)

@router.get("/getbyId")
def getById(Id:str,cuurent_user = Depends(utils.get_current_user)):
    return product.getById(Id,cuurent_user)