from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.dependencies.database import get_db
from app.modules.user.schema import UserCreate, UserRead
from app.modules.user.service import get_user_service
from app.modules.user.model import User

class AuthService:
  def __init__(self, db: Session):
    self.db = db
  
  def register(self, user_data: UserCreate):
    user_service = get_user_service(self.db)
    new_user = user_service.create(user_data=user_data)

    if not new_user:
      return None
    
    return new_user

  def login(self, login_form_data: OAuth2PasswordRequestForm = Depends()):
    user = self.db.query(User).filter(
        (User.email == login_form_data.username) | (User.username == login_form_data.username)
    ).first()
    if not user or not verify_password(login_form_data.password, user.password):
      return None
    
    token = create_access_token({"sub": str(user.id)})
    user_json = UserRead.model_validate(user).model_dump()
    return {"user": user_json, **token}

def get_auth_service(db: Session = Depends(get_db)):
  return AuthService(db)