from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Base, Mixin
from app.db.association import user_friend

class Friend(Base, Mixin):
	__tablename__ = "friend"

	id: Mapped[uuid4pk]
	name: Mapped[name]
	username = Column(String(30), unique=True, index=True, nullable=False)
	photo_url = Column(String, nullable=True)

	users = relationship("User", secondary=user_friend, back_populates="friends")