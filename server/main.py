from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.friend.router import router as friend_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(friend_router, prefix="/friend", tags=["friend"])