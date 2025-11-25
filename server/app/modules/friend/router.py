from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile
from app.core.responses import APIResponse
from app.dependencies.auth import get_current_user
from app.modules.friend.schema import FriendCreate
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

@router.get("/requests")
def get_friend_requests(
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friends = friend_service.list_requests(user_id=current_user.id)
  return APIResponse.success(
    message="Fetched friends successfully.",
    data=friends
  )

@router.post("/accept-request/{friend_id}")
def accept_friend_request(
  friend_id: UUID,
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friend = friend_service.accept_friend_request(user=current_user, friend_id=friend_id)
  return APIResponse.success(
    message="Friend request accepted successfully.",
    data=friend
  )

@router.post("/reject-request/{friend_id}")
def reject_friend_request(
  friend_id: UUID,
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friend_service.reject_friend_request(user_id=current_user.id, friend_id=friend_id)
  return APIResponse.success(
    message="Friend request rejected successfully.",
    data=None
  )

@router.post("/add")
def add_friend(
  username: str,
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friend = friend_service.add(user=current_user, username=username)
  return APIResponse.success(
    message="Friend added successfully.",
    data=friend
  )

@router.post("/create")
def create_friend(
  friend_data = Depends(FriendCreate),
  profile_photo: UploadFile = None,
  friend_service: FriendService = Depends(get_friend_service),
  current_user=Depends(get_current_user)
):
  friend = friend_service.create(user=current_user, friend_data=friend_data, profile_photo=profile_photo)
  return APIResponse.success(
    message="Friend created successfully.",
    data=friend
  )