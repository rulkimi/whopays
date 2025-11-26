from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Base, Mixin
from sqlalchemy import Enum
from app.modules.friend.schema import ContactType, FriendshipStatus

class ExternalContact(Base, Mixin):
  __tablename__ = "external_contact"

  id: Mapped[uuid4pk]
  name: Mapped[name]
  email = Column(String, nullable=True)
  phone = Column(String, nullable=True)
  photo_url = Column(String, nullable=True)

  friendships = relationship("Friendship", back_populates="external_contact")

class Friendship(Base):
	__tablename__ = "friendship"

	id: Mapped[uuid4pk]

	user_id = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("user.id", ondelete="CASCADE"),
		nullable=False,
		index=True
	)

	contact_type = Column(Enum(ContactType), nullable=False)

	friend_user_id = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("user.id", ondelete="CASCADE"),
		nullable=True,
		index=True
	)

	external_contact_id = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("external_contact.id", ondelete="CASCADE"),
		nullable=True,
		index=True
	)

	status = Column(
		Enum(FriendshipStatus),
		nullable=False,
		default=FriendshipStatus.pending
	)

	user = relationship(
		"User",
		back_populates="friendships",
		foreign_keys=[user_id]
	)

	friend_user = relationship(
		"User",
		foreign_keys=[friend_user_id]
	)

	external_contact = relationship(
		"ExternalContact",
		back_populates="friendships"
	)
