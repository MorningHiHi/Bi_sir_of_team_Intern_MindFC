from sqlalchemy import Column, Integer, String,DECIMAL,Boolean
from db.database import Base
from passlib.hash import bcrypt
from uuid import uuid4, UUID
from typing import Optional,List

MAX_BCRYPT_LENGTH = 72 

from sqlalchemy import (
    Column, Integer, String, Text, Enum, ForeignKey, Date, DateTime, DECIMAL, func, UniqueConstraint,Index,Computed
)
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped

#Base = declarative_base()


class User(Base):
    
    __tablename__ = "user"

    id = Column(String(255), primary_key=True, index=True)
    # id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    username = Column(String(255))
    password = Column(String(255))
    def verify_password(self, password: str) -> bool:
        truncated_password = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
        return bcrypt.verify(truncated_password, self.password)

    def set_password(self, password: str):
       truncated_password = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
       self.password = bcrypt.hash(truncated_password)


class Category(Base):
    __tablename__ = "category"

    id:Mapped[UUID] = mapped_column(primary_key=True,index=True)
    name:Mapped[str] = mapped_column(String(50),unique=True)
    product: Mapped[List["Product"]] = relationship(back_populates="category")

class Product(Base):
    __tablename__ = "product"

    id: Mapped[UUID] = mapped_column(primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    Category_id = mapped_column(ForeignKey("category.id"))

    category: Mapped[Category] = relationship(back_populates="product")