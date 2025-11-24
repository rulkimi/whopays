from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_hashed_password
from app.dependencies.database import get_db
from app.modules.user.model import User
from app.modules.user.schema import UserCreate, UserRead

class UserService:
  def __init__(self, db: Session):
    self.db = db
  
  def get_user(self, **filters):
    return self.db.query(User).filter_by(**filters).first()

  def create(self, user_data: UserCreate):
    user_by_email = self.get_user(email=user_data.email)
    user_by_username = self.get_user(username=user_data.username)
    errors = {}
    if user_by_email:
      errors["email"] = "Email already registered"
    if user_by_username:
      errors["username"] = "Username already taken"
    if errors:
      raise ValueError(errors)

    try:
      hashed_password = get_hashed_password(user_data.password)
      new_user = User(
        email=user_data.email,
        username=user_data.username,
        name=user_data.name,
        password=hashed_password
      )
      self.db.add(new_user)
      self.db.commit()
      self.db.refresh(new_user)
      return UserRead.model_validate(new_user).model_dump()
    except Exception as e:
      self.db.rollback()
      # Log error or handle as needed
      raise RuntimeError("Failed to create user") from e
      
def get_user_service(db: Session = Depends(get_db)):
  return UserService(db)