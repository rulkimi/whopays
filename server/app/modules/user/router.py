from fastapi import APIRouter, Depends, status

from app.core.responses import APIResponse
from app.modules.user.schema import UserCreate
from app.modules.user.service import UserService, get_user_service

router = APIRouter()

@router.post("/register")
def register_user(
	user_data: UserCreate,
	user_service: UserService = Depends(get_user_service)
):
  try:
    new_user = user_service.register(user_data=user_data)
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

  except Exception as e:
    return APIResponse.error(
      message=f"Unable to register user right now: {e}",
      code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )