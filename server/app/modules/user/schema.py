from fastapi import Body, UploadFile
from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
  username: str
  name: str
  email: str

class UserCreate(UserBase):
  password: str

class UserRead(UserBase):
  id: UUID
  photo_url: str

  class Config:
    from_attributes = True

