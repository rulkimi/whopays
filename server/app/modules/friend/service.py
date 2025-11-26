from uuid import UUID
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.file import get_file_service
from app.modules.user.service import get_user_service
from app.modules.user.schema import UserRead
from app.modules.user.model import User

from app.modules.friend.model import (
	ExternalContact,
	Friendship,
	FriendshipStatus,
	ContactType
)
from app.modules.friend.schema import (
	FriendAdd,
	FriendCreate,
	FriendRead
)


class FriendService:
	def __init__(self, db: Session):
		self.db = db

	def list(self, user_id: UUID):
		friends = (
			self.db.query(Friendship)
			.filter(Friendship.user_id == user_id)
			.filter(Friendship.status == FriendshipStatus.accepted)
			.all()
		)

		result = []
		for f in friends:
			if f.contact_type == ContactType.user:
				friend = f.friend_user
			else:
				friend = f.external_contact

			result.append(FriendRead.model_validate(friend).model_dump())

		return result

	def list_requests(self, user_id: UUID):
		incoming = (
			self.db.query(Friendship)
			.filter(Friendship.friend_user_id == user_id)
			.filter(Friendship.status == FriendshipStatus.pending)
			.all()
		)

		outgoing = (
			self.db.query(Friendship)
			.filter(Friendship.user_id == user_id)
			.filter(Friendship.status == FriendshipStatus.pending)
			.all()
		)

		incoming_json = [
			{
				"id": f.user_id,
				"name": f.user.name,
				"username": f.user.username,
				"photo_url": f.user.photo_url,
				"status": "incoming"
			}
			for f in incoming if f.contact_type == ContactType.user
		]

		outgoing_json = []
		for f in outgoing:
			if f.contact_type == ContactType.user:
				target = f.friend_user
			else:
				target = f.external_contact

			outgoing_json.append(
				{
					"id": getattr(target, "id"),
					"name": getattr(target, "name"),
					"username": getattr(target, "username", None),
					"photo_url": getattr(target, "photo_url", None),
					"status": "outgoing"
				}
			)

		return incoming_json + outgoing_json

	def add_user_friend(self, user: User, username: str):
		user_service = get_user_service(self.db)
		friend_user = user_service.get_user(username=username)

		if not friend_user:
			raise ValueError("User not found.")

		if friend_user.id == user.id:
			raise ValueError("You cannot add yourself.")

		existing = (
			self.db.query(Friendship)
			.filter(Friendship.user_id == user.id)
			.filter(Friendship.friend_user_id == friend_user.id)
			.first()
		)

		if existing:
			return {"message": "Request already exists", "status": existing.status}

		friendship = Friendship(
			user_id=user.id,
			contact_type=ContactType.user,
			friend_user_id=friend_user.id,
			status=FriendshipStatus.pending
		)

		self.db.add(friendship)
		self.db.commit()
		self.db.refresh(friendship)

		return {
			"message": "Friend request sent.",
			"status": "pending"
		}

	def add_external_contact(self, user: User, data: FriendCreate, profile_photo: UploadFile = None):
		file_service = get_file_service()
		photo_url = file_service.upload_file(profile_photo, "external_contacts") if profile_photo else None

		contact = ExternalContact(
			name=data.name,
			email=None,
			phone=None,
			photo_url=photo_url
		)

		self.db.add(contact)
		self.db.commit()
		self.db.refresh(contact)

		friendship = Friendship(
			user_id=user.id,
			contact_type=ContactType.external,
			external_contact_id=contact.id,
			status=FriendshipStatus.accepted  # no approval needed
		)

		self.db.add(friendship)
		self.db.commit()

		return FriendRead.model_validate(contact).model_dump()

	def accept_friend_request(self, user: User, requester_id: UUID):
		req = (
			self.db.query(Friendship)
			.filter(Friendship.friend_user_id == user.id)
			.filter(Friendship.user_id == requester_id)
			.filter(Friendship.status == FriendshipStatus.pending)
			.first()
		)

		if not req:
			raise ValueError("No pending friend request.")

		req.status = FriendshipStatus.accepted

		existing_reverse = (
			self.db.query(Friendship)
			.filter(Friendship.user_id == user.id)
			.filter(Friendship.friend_user_id == requester_id)
			.first()
		)

		if not existing_reverse:
			reverse = Friendship(
				user_id=user.id,
				contact_type=ContactType.user,
				friend_user_id=requester_id,
				status=FriendshipStatus.accepted
			)
			self.db.add(reverse)

		self.db.commit()

		friend = self.db.query(User).filter(User.id == requester_id).first()
		return UserRead.model_validate(friend).model_dump()

	def reject_friend_request(self, user: User, requester_id: UUID):
		req = (
			self.db.query(Friendship)
			.filter(Friendship.friend_user_id == user.id)
			.filter(Friendship.user_id == requester_id)
			.first()
		)

		if req:
			req.status = FriendshipStatus.rejected
			self.db.commit()

		return {"message": "Request rejected."}


def get_friend_service(db: Session = Depends(get_db)):
	return FriendService(db)
