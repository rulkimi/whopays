from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Base, Mixin

class User(Base, Mixin):
	__tablename__ = "user"

	id: Mapped[uuid4pk]
	name: Mapped[name]
	username = Column(String(30), unique=True, index=True, nullable=False)
	email = Column(String, unique=True, index=True, nullable=False)
	password = Column(String, nullable=False)
	photo_url = Column(String, nullable=True)

	friendships = relationship(
		"Friendship",
		back_populates="user",
		foreign_keys="Friendship.user_id"
	)
	receipts = relationship(
		"Receipt",
		back_populates="user"
	)
