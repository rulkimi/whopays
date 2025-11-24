from fastapi import APIRouter, Depends
from app.core.responses import APIResponse
from app.dependencies.auth import get_current_user
from app.modules.friend.service import FriendService, get_friend_service

router = APIRouter()

@router.get("")
def get_friends(
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friends = friend_service.list(user_id=current_user.id)
  return APIResponse.success(
    message="Fetched friends successfully.",
    data=friends
  )

@router.post("/add")
def add_friend(
  username: str,
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friend = friend_service.add(user_id=current_user.id, username=username)
  return APIResponse.success(
    message="Friend added successfully.",
    data=friend
  )