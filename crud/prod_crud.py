# crud/user_crud.py
from sqlalchemy.orm import Session, joinedload
from db import models
from schemas.product_schema import Product
from fastapi import UploadFile
import shutil
import os
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from uuid import UUID
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

    def create_product(self, iname:str,iprice:int,icate_id:UUID,idescription:str=None):
        existing = (
            self.db.query(models.Category)
            .filter((models.Category.id == icate_id))
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
            name= iname,
            description=idescription,
            price=iprice,
            Category_id=icate_id,
        )
        self.db.add(new_prod)
        self.db.commit()
        self.db.refresh(new_prod)
        return {
            "id": str(new_prod.id),
            "name": new_prod.name,
            "description": new_prod.description,
            "price": new_prod.price,
            "category": {"id": icate_id, "name": existing.name},
        }  # đoạn này name chưa trả về name thật trong bảng đc xử lý sau nhé

    # Cần thêm tham số product_id để biết sửa ai
    def put_update_Product(self, product_id: UUID, iname: str, iprice: int, icate_id: UUID, idescription: str = None):
        # 1. Tìm sản phẩm cần sửa (Thay input.id bằng product_id)
        data = (
            self.db.query(models.Product)
            .options(joinedload(models.Product.category))
            .filter(models.Product.id == product_id)
            .first()
        )
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")

        # 2. Xử lý Category (Thay input.category.id bằng icate_id)
        # Logic: Kiểm tra xem ID danh mục mới có tồn tại không
        if icate_id:
            existing_cate = self.db.query(models.Category).filter(
                models.Category.id == icate_id
            ).first()
            
            if not existing_cate:
                raise HTTPException(status_code=400, detail="New Category not found")
            
            # Gán ID mới vào data
            data.Category_id = icate_id
            # Lưu tên category để lát nữa return cho đúng (vì icate_id chỉ là số UUID)
            cate_name_for_return = existing_cate.name
        else:
            # Nếu không truyền icate_id, giữ nguyên cái cũ
            cate_name_for_return = data.category.name if data.category else None

        # 3. Update các trường còn lại (Thay vòng lặp dynamic bằng gán trực tiếp)
        # Vì giờ ta nhận tham số rời, gán trực tiếp sẽ nhanh và chuẩn hơn
        if iname is not None:
            data.name = iname
        if iprice is not None:
            data.price = iprice
        if idescription is not None:
            data.description = idescription

        # 4. Lưu và Refresh
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)

        # 5. Return kết quả
        return {
            "id": str(data.id),
            "name": data.name,
            "description": data.description,
            "price": data.price,
            # Trả về thông tin category mới nhất
            "category": {
                "id": str(data.Category_id), 
                "name": cate_name_for_return
            },
        }
    
    def del_delete_product(self,input:UUID):
        data = self.db.query(models.Product).filter(models.Product.id==input).first()
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
