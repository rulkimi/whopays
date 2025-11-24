from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Base, Mixin
from app.db.association import user_friend

class Friend(Base, Mixin):
	__tablename__ = "friend"

	id: Mapped[uuid4pk]
	name: Mapped[name]
	email = Column(String, unique=True, index=True, nullable=False)
	username = Column(String(30), unique=True, index=True, nullable=False)
	photo_url = Column(String, nullable=True)
	status = Column(String(16), default="pending", nullable=False, index=True)

	users = relationship("User", secondary=user_friend, back_populates="friends")