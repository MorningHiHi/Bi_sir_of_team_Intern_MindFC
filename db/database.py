from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from setting.config import settings
#khởi tại đối tượng engine quản lý kết nối DB
engine = create_engine(settings.DATABASE_URL, echo=settings.APP_DEBUG) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""hai dòng lệnh dưới dùng để khai báo một đối tượng dùng để quản lý các class kế thừa nó giúp cho sqlAIchemy ánh xạ các class đến các bảng tương ứng trong DB"""
#Base = declarative_base()
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
