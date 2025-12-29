from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from db.database import get_db
from controller import user
from schemas.user_schema import LoginResponse,LoginRequest,UserBase,UpdateUser
from typing import List
from setting import utils

router = APIRouter(prefix="/users", tags=["Users"])#khởi tạo đối tượng định tuyến

@router.get("")
def get_list_user(data=Depends(user.get_list_user)):
    return data


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return user.login_user(data, db)


@router.post("/", response_model=UserBase)
def create_user(data: UserBase, db: Session = Depends(get_db)):
    return user.create_new_admin(data, db)

@router.post("/user",response_model=UserBase)
def create_Newuser(data: UserBase,current_user = Depends(utils.get_current_user)):
    return user.create_new_user(data,current_user)

@router.get("/infoUser")
def info_User(data = Depends(user.list_info_user)):
    return data 

@router.put("/updateUser",response_model=UserBase)
def updateUser(data:UpdateUser ,current_user = Depends(user.get_current_user)):
    return user.put_update_user(data.id,user=data,curent_user=current_user)

@router.delete("/deleteUser")
def deleteUser(text:str, current_user = Depends(user.get_current_user)):
    return user.del_delete_user(text,curent_user=current_user)