from datetime import datetime, timezone
from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def utcnow():
  return datetime.now(timezone.utc)

class Mixin:
  @declared_attr
  def created_at(cls):
    return Column(DateTime(timezone=True), default=utcnow, nullable=False)
  
  @declared_attr
  def updated_at(cls):
    return Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

  @declared_attr
  def is_deleted(cls):
    return Column(Boolean, default=False, nullable=False)

  @declared_attr
  def deleted_at(cls):
    return Column(DateTime(timezone=True), nullable=True)