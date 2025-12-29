from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from crud import crud
from schemas.user_schema import LoginRequest,LoginResponse,UserCreate,UserBase
from setting.utils import get_offset_limit,get_pages_records,get_current_user
from db.database import get_db
from crud.crud import DatabaseApi
from crud.crud import create_user
from db.models import User
from setting.utils import create_access_token, create_refresh_token
from passlib.hash import bcrypt

def login_user(data: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token_data = {"user_id": str(user.id), "username": user.username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)

def create_new_admin(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(crud.models.User).filter(
        (crud.models.User.username == user.username) 
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return crud.create_user(db, user)


def create_new_user(user: UserCreate,current_user):
    db = DatabaseApi(current_user)
    result =db.create_Newuser(user)
    return result


def list_info_user(current_user= Depends(get_current_user)):
    db = DatabaseApi(current_user)
    return db.get_info_user()

def put_update_user(text_search:str, user: UserBase,curent_user = Depends(get_current_user)):
    db=DatabaseApi(curent_user)
    return db.put_update_user(text_search,user)

def del_delete_user(text_search:str,curent_user = Depends(get_current_user)):
    db=DatabaseApi(curent_user)
    return db.del_delete_user(text_search)


#get_current_user dùng để xác thực người dùng 
def get_list_user(text_search:str=None,current_user = Depends(get_current_user), offset_limit=Depends(get_offset_limit)):
    db = DatabaseApi(current_user)#nhận dữ liệu của DB
    offset,limit=offset_limit#lấp 
    data, total = db.get_list_user(offset,limit,text_search)
    if not data:
        raise HTTPException(status_code=404, detail="No users found")
    data=data, total
    return get_pages_records(data,offset_limit)



