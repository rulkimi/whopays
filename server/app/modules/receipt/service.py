from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.modules.receipt.model import (
	Receipt,
	ReceiptParticipant,
	ReceiptItem,
	ReceiptItemFriend,
	ReceiptItemVariation
)

from app.modules.receipt.schema import (
	ReceiptCreate,
	ReceiptRead,
	ReceiptParticipantCreate,
	ReceiptItemCreate,
	ReceiptItemFriendCreate,
	ReceiptItemVariationCreate,
	ReceiptAIExtracted,
	ai_extracted_to_receipt_create
)


class ReceiptService:
	def __init__(self, db: Session):
		self.db = db

	def list(self, user_id: UUID):
		receipts = (
			self.db.query(Receipt)
			.filter(Receipt.user_id == user_id)
			.all()
		)
		return [ReceiptRead.model_validate(r).model_dump() for r in receipts]

	def get(self, receipt_id: UUID):
		receipt = (
			self.db.query(Receipt)
			.filter(Receipt.id == receipt_id)
			.first()
		)
		if not receipt:
			raise ValueError("Receipt not found")

		return ReceiptRead.model_validate(receipt).model_dump()

	def create(self, data: ReceiptCreate):
		receipt = Receipt(
			restaurant_name=data.restaurant_name,
			subtotal=data.subtotal,
			tax=data.tax,
			service_charge=data.service_charge,
			tip=data.tip,
			rounding_amount=data.rounding_amount,
			discount=data.discount,
			total_amount=data.total_amount,
			receipt_url=data.receipt_url,
			notes=data.notes,
			user_id=data.user_id
		)

		self.db.add(receipt)
		self.db.commit()
		self.db.refresh(receipt)

		if data.participants:
			for p in data.participants:
				participant = ReceiptParticipant(
					receipt_id=receipt.id,
					is_owner=p.is_owner,
					owes_amount=p.owes_amount,
					split_method=p.split_method,
					participant_type=p.participant_type,
					user_id=p.user_id,
					external_contact_id=p.external_contact_id
				)
				self.db.add(participant)

		if data.items:
			for item_data in data.items:
				item = self._add_item(receipt.id, item_data)
				self.db.add(item)

		self.db.commit()
		self.db.refresh(receipt)
		return ReceiptRead.model_validate(receipt).model_dump()

	def create_from_ai_extract(self, user_id: UUID, extracted: ReceiptAIExtracted):
		receipt_payload = ai_extracted_to_receipt_create(
			extracted=extracted,
			user_id=user_id
		)
		return self.create(data=receipt_payload)

	def _add_item(self, receipt_id: UUID, data: ReceiptItemCreate):
		item = ReceiptItem(
			receipt_id=receipt_id,
			name=data.name,
			quantity=data.quantity,
			unit_price=data.unit_price,
			total_price=data.total_price
		)

		self.db.add(item)
		self.db.commit()
		self.db.refresh(item)

		if data.variations:
			for v in data.variations:
				variation = ReceiptItemVariation(
					item_id=item.id,
					name=v.name,
					price=v.price
				)
				self.db.add(variation)

		if data.participants:
			for p in data.participants:
				friend = ReceiptItemFriend(
					item_id=item.id,
					user_id=p.user_id,
					external_contact_id=p.external_contact_id,
					share_ratio=p.share_ratio
				)
				self.db.add(friend)

		return item

	def add_participant(self, receipt_id: UUID, data: ReceiptParticipantCreate):
		receipt = self.db.query(Receipt).filter(Receipt.id == receipt_id).first()
		if not receipt:
			raise ValueError("Receipt not found")

		participant = ReceiptParticipant(
			receipt_id=receipt.id,
			is_owner=data.is_owner,
			owes_amount=data.owes_amount,
			split_method=data.split_method,
			participant_type=data.participant_type,
			user_id=data.user_id,
			external_contact_id=data.external_contact_id
		)

		self.db.add(participant)
		self.db.commit()
		self.db.refresh(participant)

		return participant

	def add_item(self, receipt_id: UUID, data: ReceiptItemCreate):
		receipt = self.db.query(Receipt).filter(Receipt.id == receipt_id).first()
		if not receipt:
			raise ValueError("Receipt not found")

		item = self._add_item(receipt.id, data)
		self.db.commit()
		return item

	def edit_item(self, item_id: UUID, update_data: dict):
		"""
		Updates a ReceiptItem. update_data is a dict of fields to update (e.g., {"name": "Noodle", "unit_price": 9.2}).
		Returns the updated item.
		"""
		item = self.db.query(ReceiptItem).filter(ReceiptItem.id == item_id).first()
		if not item:
			raise ValueError("Item not found")

		# Only update allowed fields
		allowed_fields = {"name", "quantity", "unit_price", "total_price"}
		updated = False
		for key, value in update_data.items():
			if key in allowed_fields:
				setattr(item, key, value)
				updated = True
		if updated:
			self.db.commit()
			self.db.refresh(item)
		return item

	def edit_receipt(self, receipt_id: UUID, update_data: dict):
		"""
		Updates Receipt fields (such as restaurant_name, subtotal, notes, etc.).
		update_data is a dict of fields to update.
		Returns the updated receipt.
		"""
		receipt = self.db.query(Receipt).filter(Receipt.id == receipt_id).first()
		if not receipt:
			raise ValueError("Receipt not found")
		
		allowed_fields = {
			"restaurant_name",
			"subtotal",
			"tax",
			"service_charge",
			"tip",
			"rounding_amount",
			"discount",
			"total_amount",
			"receipt_url",
			"notes"
		}
		updated = False
		for key, value in update_data.items():
			if key in allowed_fields:
				setattr(receipt, key, value)
				updated = True
		if updated:
			self.db.commit()
			self.db.refresh(receipt)
		return ReceiptRead.model_validate(receipt).model_dump()

	def add_item_participant(self, item_id: UUID, data: ReceiptItemFriendCreate):
		item = self.db.query(ReceiptItem).filter(ReceiptItem.id == item_id).first()
		if not item:
			raise ValueError("Item not found")

		friend = ReceiptItemFriend(
			item_id=item.id,
			user_id=data.user_id,
			external_contact_id=data.external_contact_id,
			share_ratio=data.share_ratio
		)

		self.db.add(friend)
		self.db.commit()
		self.db.refresh(friend)
		return friend

	def add_item_variation(self, item_id: UUID, data: ReceiptItemVariationCreate):
		item = self.db.query(ReceiptItem).filter(ReceiptItem.id == item_id).first()
		if not item:
			raise ValueError("Item not found")

		variation = ReceiptItemVariation(
			item_id=item.id,
			name=data.name,
			price=data.price
		)

		self.db.add(variation)
		self.db.commit()
		self.db.refresh(variation)
		return variation

	def delete(self, receipt_id: UUID):
		receipt = self.db.query(Receipt).filter(Receipt.id == receipt_id).first()
		if not receipt:
			raise ValueError("Receipt not found")

		self.db.delete(receipt)
		self.db.commit()
		return {"message": "Receipt deleted successfully"}


def get_receipt_service(db: Session = Depends(get_db)):
	return ReceiptService(db)
