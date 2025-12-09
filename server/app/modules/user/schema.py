from fastapi import Body, UploadFile, Form
from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
  username: str
  name: str
  email: str


class UserCreate(UserBase):
  password: str

  @classmethod
  def as_form(
    cls,
    username: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
  ):
    return cls(username=username, name=name, email=email, password=password)

class UserRead(UserBase):
  id: UUID
  photo_url: str

  class Config:
    from_attributes = True

