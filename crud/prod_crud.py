# crud/user_crud.py
from sqlalchemy.orm import Session, joinedload
from db import models
from schemas.product_schema import Product
from fastapi import UploadFile
import shutil
import os
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
import uuid

"""
nội dung file này tập trung vào các truy vấn trong DB thông qua các truy vấn lười của sqlAIchemy, trả về các dữ liệu
"""


class DatabaseProduct:
    def __init__(self, current_user):
        db, token_data, _ = current_user
        self.db: Session = db
        self.user = token_data

    def get_list_product(
        self,
        offset: int = None,
        limit: int = None,
        text_search: str = None,
    ):
        data = self.db.query(models.Product)
        if text_search is not None:
            data = data.filter(models.Product.name.ilike(f"%{text_search.lower()}%"))
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
                "price": record.price,
                "decription":record.description,
                "categoty_id":record.Category_id
            }
            for record in data
            # trả về các bản ghi trong data ở dạng json theo cấu trúc của dòng trên
        ]  # rc sẽ là một mảng có các bảng ghi là json
        return rc, total

    def create_product(self, input: Product):
        existing = (
            self.db.query(models.Category)
            .filter((models.Category.id == input.category.id))
            .first()
        )
        # kiểm tra người đã tồn tại hay chưa
        if not existing:
            raise HTTPException(status_code=400, detail="Category ID is required")
        # existing = (
        #     self.db.query(models.Product)
        #     .filter((models.Product.id == input.id))
        #     .first()
        # )
        # if existing:
        #     raise HTTPException(status_code=400, detail="product already exists")

        new_prod = models.Product(
            id=uuid.uuid4(),
            name=input.name,
            description=input.description,
            price=input.price,
            Category_id=input.category.id,
        )
        self.db.add(new_prod)
        self.db.commit()
        self.db.refresh(new_prod)
        return {
            "id": str(new_prod.id),
            "name": new_prod.name,
            "description": new_prod.description,
            "price": new_prod.price,
            "category": {"id": input.category.id, "name": input.category.name},
        }  # đoạn này name chưa trả về name thật trong bảng đc xử lý sau nhé

    def put_update_Product(self, input: Product):
        data = (
            self.db.query(models.Product)
            .options(joinedload(models.Product.category))
            .filter(models.Product.id == input.id)
            .first()
        )
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")

        update_data = input.model_dump(exclude_unset=True)
        if "id" in update_data:
            del update_data["id"]

        # Loại bỏ 'category' object nếu có (vì ta update qua category_id)
        # Nếu schema input của bạn có lồng object category, phải xử lý riêng category_id
        if "category" in update_data:
            # Nếu logic của bạn cho phép đổi danh mục:
            existing = self.db.query(models.Category).filter(
                models.Category.id == input.category.id
            ).first()
            if not existing:
                raise HTTPException(status_code=400, detail="New Category not found")
            data.category_id = input.category.id
            del update_data["category"]

        # 3. Vòng lặp update tự động (Dynamic Update)
        # key: tên cột (name, price...), value: giá trị mới
        for key, value in update_data.items():
            # setattr(obj, name, value) tương đương với product_db.name = value
            setattr(data, key, value)
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return {
            "id": str(data.id),
            "name": data.name,
            "description": data.description,
            "price": data.price,
            "category": {"id": input.category.id, "name": input.category.name},
        }
    
    def del_delete_product(self,input:Product):
        data = self.db.query(models.Product).filter(models.Product.id==input.id).first()
        if not data :
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(data)
        self.db.commit()
        return {
            "details":"Deleted successfully",
            "id_delete": data.id
        }
    
    def getById(self,id:str):
        data = self.db.query(models.Product).filter(models.Product.id==id).first()
        if not data :
            raise HTTPException(status_code=404, detail="User not found")
        id_cate=data.Category_id

        data_cate=self.db.query(models.Category).filter(models.Category.id==id_cate).first()

        rc={
            "id":str(data.id),
            "name":data.name,
            "price":data.price,
            "description":data.description,
            "category":{
                "id":str(data_cate.id),
                "name":data_cate.name
            }
        }
        return rc
