from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_hashed_password
from app.dependencies.database import get_db
from app.modules.user.model import User
from app.modules.user.schema import UserCreate, UserRead

class UserService:
  def __init__(self, db: Session):
    self.db = db
  
  def list(self, **filters):
    return self.db.query(User).filter_by(**filters).first()

  def register(self, user_data: UserCreate):
    user = self.list(email=user_data.email)
    if user:
      return None
    
    hashed_password = get_hashed_password(user_data.password)
    new_user = User(
      email=user_data.email,
      name=user_data.name,
      password=hashed_password
    )
    self.db.add(new_user)
    self.db.commit()
    self.db.refresh(new_user)
    new_user_json = UserRead.model_validate(new_user).model_dump()
    return new_user_json
      
def get_user_service(db: Session = Depends(get_db)):
  return UserService(db)