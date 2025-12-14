from sqlalchemy import Column, Integer, String,DECIMAL,Boolean
from db.database import Base
from passlib.hash import bcrypt

MAX_BCRYPT_LENGTH = 72 

from sqlalchemy import (
    Column, Integer, String, Text, Enum, ForeignKey, Date, DateTime, DECIMAL, func, UniqueConstraint,Index,Computed
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255))
    password = Column(String(255))
    def verify_password(self, password: str) -> bool:
        truncated_password = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
        return bcrypt.verify(truncated_password, self.password)

    def set_password(self, password: str):
       truncated_password = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
       self.password = bcrypt.hash(truncated_password)

