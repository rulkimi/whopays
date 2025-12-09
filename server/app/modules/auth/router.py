from fastapi import APIRouter, Depends, Query, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.responses import APIResponse
from app.modules.user.schema import UserCreate
from app.modules.auth.service import AuthService, get_auth_service

router = APIRouter()

@router.post("/register")
def register_user(
	user_data: UserCreate = Depends(UserCreate.as_form),
  profile_photo: UploadFile = None,
	auth_service: AuthService = Depends(get_auth_service)
):
  new_user = auth_service.register(user_data=user_data, profile_photo=profile_photo)
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
  auth_service: AuthService = Depends(get_auth_service),
  swagger_auth: bool = Query(False)
):
  login_data = auth_service.login(form_data)
  if not login_data:
    return APIResponse.error(
      message="Invalid email or password.",
      code=status.HTTP_401_UNAUTHORIZED
    )
  
  if swagger_auth:
    return {**login_data}
  else:  
    return APIResponse.success(
      message="User logged in successfully",
      data=login_data,
      code=status.HTTP_200_OK
    )

@router.post("/refresh")
def refresh_access_token(
  refresh_token: str = Query(..., description="Refresh token"),
  auth_service: AuthService = Depends(get_auth_service)
):
  try:
    refreshed_data = auth_service.refresh_token(refresh_token)
    return APIResponse.success(
      message="Access token refreshed successfully",
      data=refreshed_data,
      code=status.HTTP_200_OK
    )
  except Exception as e:
    return APIResponse.error(
      message=str(e),
      code=status.HTTP_401_UNAUTHORIZED
    )
