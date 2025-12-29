from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from crud import crud
from schemas.product_schema import Product
from setting.utils import get_offset_limit,get_pages_records,get_current_user
from db.database import get_db
from crud.prod_crud import DatabaseProduct
from db.models import User
from setting.utils import create_access_token, create_refresh_token
from passlib.hash import bcrypt

def get_list_product(text_search:str=None,current_user = Depends(get_current_user), offset_limit=Depends(get_offset_limit)):
    db = DatabaseProduct(current_user)#nhận dữ liệu của DB
    offset,limit=offset_limit#lấp 
    data, total = db.get_list_product(offset,limit,text_search)
    if not data:
        raise HTTPException(status_code=404, detail="No users found")
    data=data, total
    return get_pages_records(data,offset_limit)


def create_product(input:Product,current_user):
    db = DatabaseProduct(current_user)
    result =db.create_product(input.name,input.price,input.category.id,input.description)
    return result

def put_update_product(input: Product,current_user ):
    db=DatabaseProduct(current_user)
    return db.put_update_Product(input.id,input.name,input.price,input.category.id,input.description)

def del_delete_product(text_search:Product,current_user):
    db=DatabaseProduct(current_user)
    return db.del_delete_product(text_search.id)

def getById(id:str,current_user):
    db=DatabaseProduct(current_user)
    return db.getById(id)