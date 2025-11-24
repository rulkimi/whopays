from sqlalchemy import Column, ForeignKey, Table
from app.db.mixin import Base

user_friend = Table(
  "user_friend",
  Base.metadata,
  Column("user_id", ForeignKey("user.id"), primary_key=True),
  Column("friend_id", ForeignKey("friend.id"), primary_key=True)
)