from sqlalchemy.orm import Session
from db import models
from schemas import user_schema
from fastapi import UploadFile
import shutil
import os
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
import uuid
from schemas.category_schema import CreateIDN,IDN,IdIDN


class databaseCategory:
    def __init__(self, curent_user):
        db, token_data, _ = curent_user
        self.db: Session = db
        self.user = token_data

    def create_category(self, data: CreateIDN):
        existing = (
            self.db.query(models.Category)
            .filter((models.Category.name == data.name))
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Category Name already exists")
        else:
            new_cate = models.Category(
                id=uuid.uuid4(),
                name=data.name,
            )
            self.db.add(new_cate)
            self.db.commit()
            self.db.refresh(new_cate)
            return new_cate

    def get_list_category(
        self,
        offset: int = None,
        limit: int = None,
        text_search: str = None,
    ):
        data = self.db.query(models.Category)
        if text_search is not None:
            data = data.filter(models.Category.name.ilike(f"%{text_search.lower()}%"))
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
                "name": record.name,
            }
            for record in data
            # trả về các bản ghi trong data ở dạng json theo cấu trúc của dòng trên
        ]  # rc sẽ là một mảng có các bảng ghi là json
        return rc, total


    def put_update_category(self,dataNew:IDN):
        data = self.db.query(models.Category).filter(models.Category.id==dataNew.id).first()
        if not data :
            raise HTTPException(status_code=404, detail="Category not found")
        data.name = dataNew.name
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return {
            "id":str(data.id),
            "name":data.name
        }
    
    def del_delete_category(self,text_search: IdIDN):
        data = self.db.query(models.Category).filter(models.Category.id==text_search.id).first()
        if not data :
            raise HTTPException(status_code=404, detail="Category not found")
        self.db.delete(data)
        self.db.commit()
        return {
            "details":"Deleted successfully",
            "id_delete": data.id,
            "name_delete": data.name
        }
    
    def get_category_byId(self,idsearch:str):
        data = self.db.query(models.Category).filter(models.Category.id==idsearch).first()
        if not data:
            raise HTTPException(status_code=404,detail="category not found")
        else: return {
            "id":str(data.id),
            "name": data.name
        }

"""
lưu ý các code trong này bị lặp khá nhiều do copy/paste dựa trên các code core để làm nhanh vấn các yêu cầu
thời gian sau cần phải viết lại các hàm có thể tái sử dụng, hoặc các class chứa các query thường dùng
các đoạn code 

data = self.db.query(models.Category).filter(models.Category.id==idsearch).first()
        if not data:
            raise HTTPException(status_code=404,detail="category not found")

bị trùng lặp trong ba hàm như get_category_byId,del_delete_category, put_update_category
"""