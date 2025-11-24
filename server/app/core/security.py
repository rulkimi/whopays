from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.settings import Settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
  return password_context.hash(password)

def create_access_token(data: dict, expires_delta: int = None):
  to_encode = data.copy()
  expires_time = expires_delta or Settings.JWT_EXPIRY_MINUTES
  expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=expires_time)
  to_encode.update({ "exp" : expire })
  enconded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
  return enconded_jwt