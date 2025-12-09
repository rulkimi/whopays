from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password, decode_refresh_token
from app.dependencies.database import get_db
from app.modules.user.schema import UserCreate, UserRead
from app.modules.user.service import get_user_service
from app.modules.user.model import User
from app.core.responses import AppException

class AuthService:
	def __init__(self, db: Session):
		self.db = db

	def register(self, user_data: UserCreate, profile_photo: UploadFile = None):
		user_service = get_user_service(self.db)
		try:
			return user_service.create(user_data=user_data, profile_photo=profile_photo)
		except AppException as e:
			raise e
		except Exception as e:
			raise AppException(message="Failed to register user", code=500)

	def login(self, login_form_data: OAuth2PasswordRequestForm = Depends()):
		user = (
			self.db.query(User)
			.filter(
				(User.email == login_form_data.username)
				| (User.username == login_form_data.username)
			)
			.first()
		)
		if not user:
			raise AppException(message="Invalid email or username.", code=401)
		if not verify_password(login_form_data.password, user.password):
			raise AppException(message="Invalid password.", code=401)

		token = create_access_token({"sub": str(user.id)})
		user_json = UserRead.model_validate(user).model_dump()
		return {"user": user_json, **token}

	def refresh_token(self, refresh_token: str):
		try:
			payload = decode_refresh_token(refresh_token)
			user_id = payload.get("sub")
			if not user_id:
				raise AppException(message="Invalid refresh token.", code=401)
			
			user = self.db.query(User).filter(User.id == user_id).first()
			if not user:
				raise AppException(message="User not found.", code=401)
			
			user_json = UserRead.model_validate(user).model_dump()

			access_token_data = create_access_token({"sub": str(user.id)})
			result = {
				"user": user_json,
				"access_token": access_token_data["access_token"],
				"access_token_expiry": access_token_data["access_token_expiry"],
				"refresh_token": refresh_token,
				"refresh_token_expiry": payload.get("exp"),
			}
			return result

		except AppException as e:
			raise e
		except Exception:
			raise AppException(message="Invalid or expired refresh token.", code=401)

def get_auth_service(db: Session = Depends(get_db)):
	return AuthService(db)