from fastapi import FastAPI, Request
from app.core.responses import APIResponse, AppException
from app.modules.auth.router import router as auth_router
from app.modules.friend.router import router as friend_router

app = FastAPI()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
  return APIResponse.error(
    message=str(exc),
    code=400
  )

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
  return APIResponse.error(
    message=exc.message,
    code=exc.code,
    data=exc.data,
    errors=exc.errors
  )

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(friend_router, prefix="/friends", tags=["Friends"])