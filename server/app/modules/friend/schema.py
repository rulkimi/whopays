from uuid import UUID

from pydantic import BaseModel
from app.modules.user.schema import UserRead

class FriendAdd(BaseModel):
  username: str

class FriendRead(UserRead):
  user_id: UUID

  class Config:
    from_attributes = True