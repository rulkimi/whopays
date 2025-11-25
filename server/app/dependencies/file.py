from datetime import timedelta
import uuid
from fastapi import UploadFile

from app.core.settings import settings
from app.dependencies.storage import minio_client

class FileService:
  @staticmethod
  def upload_file(file: UploadFile, folder: str) -> str:
    safe_filename = file.filename.replace(" ", "-")
    file_id = f"{folder}-{uuid.uuid4()}-{safe_filename}"

    file.file.seek(0)

    # Calculate length safely
    file.file.seek(0, 2)  # Move to end of file
    file_length = file.file.tell()
    file.file.seek(0)     # Reset to start

    minio_client.put_object(
      bucket_name=settings.MINIO_BUCKET,
      object_name=file_id,
      data=file.file,  # pass the file-like object directly
      length=file_length,
      part_size=10 * 1024 * 1024
    )

    return file_id

  @staticmethod
  def download_file(file_id: str):
    response = minio_client.get_object(settings.MINIO_BUCKET, file_id)
    return response.read()
  
  @staticmethod
  def generate_presinged_url(file_id: str, expiry_minutes: int = 10):
    raw_url = minio_client.presigned_get_object(
      settings.MINIO_BUCKET,
      file_id,
      expires=timedelta(minutes=expiry_minutes)
    )
    return raw_url

def get_file_service():
  return FileService()