# crud/user_crud.py
from sqlalchemy.orm import Session
from db import models
from schemas import user_schema
from fastapi import UploadFile
import shutil
import os
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
import uuid

"""
nội dung file này tập trung vào các truy vấn trong DB thông qua các truy vấn lười của sqlAIchemy, trả về các dữ liệu
"""


class DatabaseApi:
    def __init__(self, current_user):
        db, token_data, _ = current_user
        self.db: Session = db
        self.user = token_data

    def get_list_user(
        self,
        offset: int = None,
        limit: int = None,
        text_search: str = None,
    ):
        data = self.db.query(models.User)
        if text_search is not None:
            data = data.filter(models.User.username.ilike(f"%{text_search.lower()}%"))
        total = (
            data.count()
        )  # bắt đầu một truy vấn , đếm xem có bao nhiêu bảng ghi trong đó
        if offset != None and limit != None:  # phần này thực hiện phân trang
            data = data.offset(offset).limit(limit)
        data = (
            data.all()
        )  # bắt đầu thực hiện all truy vấn, sau đó data là một list user
        rc = [
            {
                "id": str(record.id),
                "username": record.username,
            }
            for record in data
            # trả về các bản ghi trong data ở dạng json theo cấu trúc của dòng trên
        ]  # rc sẽ là một mảng có các bảng ghi là json
        return rc, total

    def create_Newuser(self, user: user_schema.UserCreate):
        existing = (
            self.db.query(models.User)
            .filter((models.User.username == user.username))
            .first()
        )
        # kiểm tra người đã tồn tại hay chưa
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        else:
            new_user = models.User(
                id=str(uuid.uuid4()),
                username=user.username,
            )
            new_user.set_password(user.password)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user

    def put_update_user(self,text_search: str = None,user = user_schema.UserCreate):
        data = self.db.query(models.User).filter(models.User.id==text_search).first()
        if not data :
            raise HTTPException(status_code=404, detail="User not found")
        data.username = user.username
        data.set_password(user.password)
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    
    def del_delete_user(self,text_search: str = None):
        data = self.db.query(models.User).filter(models.User.id==text_search).first()
        if not data :
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(data)
        self.db.commit()
        return {
            "details":"Deleted successfully",
            "id_delete": data.id
        }


    def get_info_user(self):
        data = self.db.query(models.User).filter(models.User.username==self.user["username"]).first()
        #data=data.all()
        return {
                "id": str(data.id),
                "username": data.username,
            }
    


def create_user(db: Session, user: user_schema.UserCreate):
    new_user = models.User(
        id=str(uuid.uuid4()),
        username=user.username,
    )
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
