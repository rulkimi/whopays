import enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from app.modules.user.schema import UserRead

class FriendshipStatus(str, enum.Enum):
  pending = "pending"
  accepted = "accepted"
  rejected = "rejected"

class ContactType(str, enum.Enum):
  user = "user"
  external = "external"

class FriendAdd(BaseModel):
  username: str

class FriendCreate(BaseModel):
  name: str

class FriendRead(UserRead):
  photo_url: str
  friend_user_id: Optional[UUID] = None
  external_contact_id: Optional[UUID] = None
  email: Optional[str] = None
  username: Optional[str] = None

  class Config:
    from_attributes = True