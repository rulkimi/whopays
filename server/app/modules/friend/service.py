from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.modules.friend.model import Friend
from app.modules.friend.schema import FriendRead
from app.modules.user.schema import UserRead
from app.modules.user.service import get_user_service
from app.modules.user.model import User
from app.db.association import user_friend

class FriendService:
	def __init__(self, db: Session):
		self.db = db

	def list(self, user_id: UUID):
		friends = (
			self.db.query(Friend)
			.join(user_friend, Friend.friend_user_id == user_friend.c.friend_id)
			.filter(user_friend.c.user_id == user_id)
			.all()
		)
		friends_json = [FriendRead.model_validate(friend).model_dump() for friend in friends]
		return friends_json

	def list_requests(self, user_id: UUID):
		users = (
			self.db.query(User)
			.join(user_friend, User.id == user_friend.c.user_id)
			.filter(user_friend.c.friend_id == user_id)
			.all()
		)
		return [
			{
				"id": user.id,
				"name": user.name,
				"email": user.email,
				"username": user.username,
				"photo_url": getattr(user, "photo_url", None),
				"status": "incoming"
			}
			for user in users
		]
	
	def add(self, user_id: UUID, username: str):
		user_service = get_user_service(self.db)
		friend_user = user_service.get_user(username=username)
		if not friend_user:
			raise ValueError("User not found.")

		user = self.db.query(User).filter_by(id=user_id).first()
		if not user:
			raise ValueError("Current user not found.")

		friend = self.db.query(Friend).filter_by(username=username).first()
		if not friend:
			friend = Friend(
        friend_user_id=friend_user.id,
				name=friend_user.name,
				email=friend_user.email,
				username=friend_user.username,
				photo_url=getattr(friend_user, "photo_url", None)
			)
			self.db.add(friend)
			self.db.commit()
			self.db.refresh(friend)

		if friend not in user.friends:
			user.friends.append(friend)
			self.db.commit()

		return FriendRead.model_validate(friend).model_dump()

def get_friend_service(db: Session = Depends(get_db)):
  return FriendService(db)