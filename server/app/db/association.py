from sqlalchemy import Column, ForeignKey, Table, String
from app.db.mixin import Base

user_friend = Table(
	"user_friend",
	Base.metadata,
	Column("user_id", ForeignKey("user.id"), primary_key=True),
	Column("friend_id", ForeignKey("friend.friend_user_id"), primary_key=True),
	Column("status", String(20), nullable=False, default="pending"),
)