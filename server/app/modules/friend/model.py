from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Base, Mixin
from app.db.association import user_friend

class Friend(Base, Mixin):
	__tablename__ = "friend"

	id: Mapped[uuid4pk]
	name: Mapped[name]
	friend_user_id = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("user.id", ondelete="CASCADE"),
		unique=True,
		index=True,
		nullable=False
	)
	email = Column(String, unique=True, index=True, nullable=False)
	username = Column(String(30), unique=True, index=True, nullable=False)
	photo_url = Column(String, nullable=True)
	status = Column(String(16), default="pending", nullable=False, index=True)

	users = relationship("User", secondary=user_friend, back_populates="friends")