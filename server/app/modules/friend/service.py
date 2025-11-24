from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.modules.friend.model import Friend
from app.modules.user.schema import UserRead
from app.modules.user.service import get_user_service
from app.modules.user.model import User
from app.db.association import user_friend

class FriendService:
  def __init__(self, db: Session):
    self.db = db
  
  def add(self, user_id: UUID, username: str):
    user_service = get_user_service(self.db)
    friend_user = user_service.get_user(username=username)
    if not friend_user:
      raise ValueError("User not found.")

    user = self.db.query(User).filter_by(id=user_id).first()
    if not user:
      raise ValueError("Current user not found.")

    friend = self.db.query(Friend).filter_by(username=username).first()
    if not friend:
      friend = Friend(
        name=friend_user.name,
        username=friend_user.username,
        photo_url=getattr(friend_user, "photo_url", None),
      )
      self.db.add(friend)
      self.db.commit()
      self.db.refresh(friend)

    if friend not in user.friends:
      user.friends.append(friend)
      self.db.commit()

def get_friend_service(db: Session = Depends(get_db)):
  return FriendService(db)