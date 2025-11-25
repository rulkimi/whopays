from uuid import UUID
import uuid
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import insert

from app.dependencies.database import get_db
from app.dependencies.file import get_file_service
from app.modules.friend.model import Friend
from app.modules.friend.schema import FriendCreate, FriendRead
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
			.join(user_friend, (Friend.friend_user_id == user_friend.c.friend_id) | (Friend.id == user_friend.c.friend_id))
			.filter(user_friend.c.user_id == user_id)
			.all()
		)
		friends_json = [FriendRead.model_validate(friend).model_dump() for friend in friends]
		return friends_json

	def list_requests(self, user_id: UUID):
		current_user_friend_id = self.db.query(Friend.id).filter(Friend.friend_user_id == user_id)
		users = (
			self.db.query(User)
			.join(user_friend, User.id == user_friend.c.user_id)
			.filter(user_friend.c.friend_id == current_user_friend_id)
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
	
	def add(self, user, username: str):
		user_service = get_user_service(self.db)
		friend_user = user_service.get_user(username=username)
		if not friend_user:
			raise ValueError("User not found.")

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

	def create(self, user, friend_data: FriendCreate, profile_photo: UploadFile = None):
		file_service = get_file_service()
		photo_url = file_service.upload_file(profile_photo, "friends")
		
		base_username = friend_data.name.lower().replace(" ", "_")
		unique_suffix = uuid.uuid4().hex[:8]
		unique_username = f"friend_{base_username}_{unique_suffix}"
		
		friend = Friend(
			friend_user_id=None,
			name=friend_data.name,
			username=unique_username,
			email=None,
			photo_url=photo_url
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