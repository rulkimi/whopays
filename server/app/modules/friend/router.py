from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.modules.friend.service import FriendService, get_friend_service

router = APIRouter()

@router.post("/add")
def add_friend(
  username: str,
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friend_service.add(user_id=current_user.id, username=username)