from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.modules.user.schema import UserRead
from enum import Enum

# Enums
class ParticipantType(str, Enum):
	user = "user"
	external = "external"

class SplitMethod(str, Enum):
	equal = "equal"
	weighted = "weighted"


# Receipt Item Variations
class ReceiptItemVariationBase(BaseModel):
	name: str
	price: float

class ReceiptItemVariationCreate(ReceiptItemVariationBase):
	pass

class ReceiptItemVariationRead(ReceiptItemVariationBase):
	id: UUID

	class Config:
		from_attributes = True


# Receipt Item Friend
class ReceiptItemFriendBase(BaseModel):
	share_ratio: Optional[float] = None
	user_id: Optional[UUID] = None
	external_contact_id: Optional[UUID] = None

class ReceiptItemFriendCreate(ReceiptItemFriendBase):
	pass

class ReceiptItemFriendRead(ReceiptItemFriendBase):
	id: UUID
	user: Optional[UserRead] = None
	# external_contact: Optional[ExternalContactRead] = None

	class Config:
		from_attributes = True


# Receipt Items
class ReceiptItemBase(BaseModel):
	name: str
	quantity: float
	unit_price: float
	total_price: float

class ReceiptItemCreate(ReceiptItemBase):
	variations: Optional[List[ReceiptItemVariationCreate]] = None
	participants: Optional[List[ReceiptItemFriendCreate]] = None

class ReceiptItemRead(ReceiptItemBase):
	id: UUID
	variations: List[ReceiptItemVariationRead] = []
	participants: List[ReceiptItemFriendRead] = []

	class Config:
		from_attributes = True


# Receipt Participants
class ReceiptParticipantBase(BaseModel):
	is_owner: bool = False
	owes_amount: Optional[float] = None
	split_method: SplitMethod = SplitMethod.weighted
	participant_type: ParticipantType
	user_id: Optional[UUID] = None
	external_contact_id: Optional[UUID] = None

class ReceiptParticipantCreate(ReceiptParticipantBase):
	pass

class ReceiptParticipantRead(ReceiptParticipantBase):
	id: UUID
	user: Optional[UserRead] = None

	class Config:
		from_attributes = True


# Main Receipt
class ReceiptBase(BaseModel):
	restaurant_name: str
	subtotal: float
	tax: Optional[float] = None
	service_charge: Optional[float] = None
	tip: Optional[float] = None
	rounding_amount: Optional[float] = None
	discount: Optional[float] = None
	total_amount: float
	receipt_url: Optional[str] = None
	notes: Optional[str] = None

class ReceiptCreate(ReceiptBase):
	user_id: UUID
	participants: Optional[List[ReceiptParticipantCreate]] = None
	items: Optional[List[ReceiptItemCreate]] = None

class ReceiptRead(ReceiptBase):
	id: UUID
	user_id: UUID
	participants: List[ReceiptParticipantRead] = []
	items: List[ReceiptItemRead] = []

	class Config:
		from_attributes = True
