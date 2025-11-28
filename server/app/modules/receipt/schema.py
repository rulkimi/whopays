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

class ReceiptStatus(str, Enum):
	processing = "processing"
	extracted = "extracted"
	failed = "failed"


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
	status: ReceiptStatus = ReceiptStatus.processing

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

class ReceiptAIExtractedItemVariation(BaseModel):
	name: str
	price: Optional[float] = None

class ReceiptAIExtractedItem(BaseModel):
	name: str
	price: Optional[float] = None
	variations: Optional[List[ReceiptAIExtractedItemVariation]] = None

class ReceiptAIExtracted(BaseModel):
	restaurant_name: Optional[str] = None
	subtotal: Optional[float] = None
	tax: Optional[float] = None
	service_charge: Optional[float] = None
	tip: Optional[float] = None
	rounding_amount: Optional[float] = None
	discount: Optional[float] = None
	total_amount: Optional[float] = None
	receipt_url: Optional[str] = None
	notes: Optional[str] = None
	items: List[ReceiptAIExtractedItem] = []

	class Config:
		from_attributes = True


def _safe_float(value: Optional[float], default: float = 0.0) -> float:
	return float(value) if value is not None else float(default)


def _safe_optional_float(value: Optional[float]) -> Optional[float]:
	return float(value) if value is not None else None


def ai_extracted_to_receipt_create(
	extracted: ReceiptAIExtracted,
	user_id: UUID
) -> ReceiptCreate:
	"""
	Transforms AI extracted data into a ReceiptCreate payload.
	This ensures required numeric fields fall back to sensible defaults and
	populates minimal item data when available.
	"""
	item_total = 0.0
	items: List[ReceiptItemCreate] = []

	for item in extracted.items or []:
		price = _safe_float(item.price)
		item_total += price

		variations = []
		for variation in item.variations or []:
			if variation.price is None:
				continue
			variations.append(
				ReceiptItemVariationCreate(
					name=variation.name or "Variation",
					price=_safe_float(variation.price)
				)
			)

		items.append(
			ReceiptItemCreate(
				name=item.name or "Item",
				quantity=1.0,
				unit_price=price,
				total_price=price,
				variations=variations or None
			)
		)

	subtotal = _safe_float(extracted.subtotal, item_total)
	total_amount = _safe_float(
		extracted.total_amount,
		item_total if item_total else subtotal
	)

	return ReceiptCreate(
		user_id=user_id,
		restaurant_name=extracted.restaurant_name or "Unknown Restaurant",
		subtotal=subtotal,
		tax=_safe_optional_float(extracted.tax),
		service_charge=_safe_optional_float(extracted.service_charge),
		tip=_safe_optional_float(extracted.tip),
		rounding_amount=_safe_optional_float(extracted.rounding_amount),
		discount=_safe_optional_float(extracted.discount),
		total_amount=total_amount,
		receipt_url=extracted.receipt_url,
		notes=extracted.notes,
		items=items or None
	)
