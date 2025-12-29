from fastapi import FastAPI
#from db import models
from db.database import Base
from db.database import engine
from router import user,category,product
from setting.config import settings #nhận vào dữ liệu của biến settings trong config 
from fastapi.middleware.cors import CORSMiddleware

"""
hai dòng dưới chịu trách nhiệm truy xuất đến các lớp file tương ứng để tại kết nối db 
thực thi các logic bên trong,(mở file đó lên để xem các chú thích luồng hoạt động)
"""
#models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine) #thay cho dòng trên

app = FastAPI(title=settings.APP_NAME, debug=settings.APP_DEBUG) 
#bắt đầu từ dòng này sẽ đk middleware

app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running!"}


