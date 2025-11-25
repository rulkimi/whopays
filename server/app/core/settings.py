import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  DB_DRIVER: str = os.getenv("DB_DRIVER")
  DB_HOST: str = os.getenv("DB_HOST")
  DB_USER: str = os.getenv("DB_USER")
  DB_PASSWORD: str = os.getenv("DB_PASSWORD")
  DB_NAME: str = os.getenv("DB_NAME")
  DB_PORT: str = os.getenv("DB_PORT")

  JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
  JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
  JWT_EXPIRY_MINUTES: str = os.getenv("JWT_EXPIRY_MINUTES")

  MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT")
  MINIO_PUBLIC_ENDPOINT: str = os.getenv("MINIO_PUBLIC_ENDPOINT")
  MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
  MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
  MINIO_SECURE: str = os.getenv("MINIO_SECURE")
  MINIO_BUCKET: str = os.getenv("MINIO_BUCKET")
  MINIO_API_PORT: str = os.getenv("MINIO_API_PORT")
  MINIO_CONSOLE_PORT: str = os.getenv("MINIO_CONSOLE_PORT")

  @property
  def DATABASE_URL(self) -> str:
    url = f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    return url

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()