from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.settings import Settings
from app.db.mixin import utcnow

settings = Settings()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
  return password_context.hash(password)

def create_access_token(data: dict, expires_delta: int = None):
  to_encode = data.copy()
  expires_time = expires_delta or settings.JWT_EXPIRY_MINUTES
  expire = utcnow() + timedelta(minutes=int(expires_time))
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
  
  refresh_expire = utcnow() + timedelta(days=7)
  refresh_data = data.copy()
  refresh_data.update({"exp": refresh_expire, "type": "refresh"})
  refresh_token = jwt.encode(refresh_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
  
  return {
    "access_token": encoded_jwt,
    "access_token_expiry": expire,
    "refresh_token": refresh_token,
    "refresh_token_expiry": refresh_expire
  }