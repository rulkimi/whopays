from minio import Minio
from app.core.settings import settings

minio_client = Minio(
  endpoint=settings.MINIO_ENDPOINT,
  access_key=settings.MINIO_ACCESS_KEY,
  secret_key=settings.MINIO_SECRET_KEY,
  secure=settings.MINIO_SECURE.lower() == "true" if isinstance(settings.MINIO_SECURE, str) else bool(settings.MINIO_SECURE)
)

if not minio_client.bucket_exists(bucket_name=settings.MINIO_BUCKET):
  minio_client.make_bucket(bucket_name=settings.MINIO_BUCKET)