from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from crud import crud
from schemas.user_schema import LoginRequest,LoginResponse,UserCreate,UserBase
from setting.utils import get_offset_limit,get_pages_records,get_current_user
from db.database import get_db
from crud.cate_crud import databaseCategory
from crud.crud import create_user
from db.models import User
from setting.utils import create_access_token, create_refresh_token
from passlib.hash import bcrypt
from schemas.category_schema import IDN,CreateIDN,IdIDN


def create_category(data:CreateIDN,current_user=Depends(get_current_user)):
    db=databaseCategory(current_user)
    result= db.create_category(data.name)
    return result

def get_list_Category(text_search:str=None,current_user = Depends(get_current_user), offset_limit=Depends(get_offset_limit)):
    db = databaseCategory(current_user)#nhận dữ liệu của DB
    offset,limit=offset_limit#lấp 
    data, total = db.get_list_category(offset,limit,text_search)
    if not data:
        raise HTTPException(status_code=404, detail="No users found")
    data=data, total
    return get_pages_records(data,offset_limit)

def put_update_Category(data:IDN,curent_user = Depends(get_current_user)):
    db=databaseCategory(curent_user)
    return db.put_update_category(data.name,data.id)

def del_delete_category(text_search:IdIDN,current_user = Depends(get_current_user)):
    db=databaseCategory(current_user)
    return db.del_delete_category(text_search.id)

def categoryById(data:str,current_user):
    db=databaseCategory(current_user)
    return db.get_category_byId(data)