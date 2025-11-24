from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Mixin

Base = declarative_base()

class User(Base, Mixin):
  __tablename__ = "user"

  id: Mapped[uuid4pk]
  name: Mapped[name]
  email = Column(String, unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
  