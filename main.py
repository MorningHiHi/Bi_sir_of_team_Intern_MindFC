from fastapi import FastAPI
from db import models
from db.database import engine
from router import user
from setting.config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.APP_DEBUG)

app.include_router(user.router)

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
