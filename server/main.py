from fastapi import FastAPI
from app.modules.user.router import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])