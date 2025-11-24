from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.responses import APIResponse
from app.modules.user.schema import UserCreate
from app.modules.auth.service import AuthService, get_auth_service

router = APIRouter()

@router.post("/register")
def register_user(
	user_data: UserCreate,
	auth_service: AuthService = Depends(get_auth_service)
):
  new_user = auth_service.register(user_data=user_data)
  if not new_user:
    return APIResponse.error(
      message=f"User with email {user_data.email} already exists.",
      code=status.HTTP_409_CONFLICT
    )
  
  return APIResponse.success(
    message="User registered successfully",
    data=new_user,
    code=status.HTTP_201_CREATED
)

@router.post("/login")
def login_user(
  form_data: OAuth2PasswordRequestForm = Depends(),
  auth_service: AuthService = Depends(get_auth_service)
):
  login_data = auth_service.login(form_data)
  if not login_data:
    return APIResponse.error(
      message="Invalid email or password.",
      code=status.HTTP_401_UNAUTHORIZED
    )
    
  # return APIResponse.success(
  #   message="User logged in successfully",
  #   data=login_data,
  #   code=status.HTTP_200_OK
  # )
  return {**login_data}