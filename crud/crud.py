# crud/user_crud.py
from sqlalchemy.orm import Session
from db import models
from schemas import user_schema
from fastapi import UploadFile
import shutil
import os
from fastapi import HTTPException,Depends
from datetime import datetime, timedelta
import uuid
class DatabaseApi:
    def __init__(self, current_user):
        db, token_data, _ = current_user
        self.db: Session = db
        self.user = token_data  

    def get_list_user(  self,
                    offset: int = None,
                    limit: int = None,
                    text_search:str=None,
    ):
        data=self.db.query(models.User)
        if text_search is not None:
            data = data.filter(models.User.username.ilike(f"%{text_search.lower()}%"))
        total = data.count()
        if offset != None and limit != None:
                data = data.offset(offset).limit(limit)
        data=data.all()
        rc = [
                {  
                    "id": str(record.id),
                    "username": record.username,
                    
                }
                for record in data
            ]
        return rc, total
    
   
    
    

def create_user(db: Session, user: user_schema.UserCreate):
    new_user = models.User(
        id=uuid.uuid4(),
        username=user.username,
    )
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
