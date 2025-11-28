from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from app.db.common_annotations import uuid4pk, name
from app.db.mixin import Base, Mixin
from app.modules.receipt.schema import ParticipantType, SplitMethod, ReceiptStatus

class Receipt(Base, Mixin):
  __tablename__ = "receipt"

  id: Mapped[uuid4pk]
  restaurant_name: Mapped[name]
  
  subtotal = Column(Float, nullable=False)
  tax = Column(Float, nullable=True)
  service_charge = Column(Float, nullable=True)
  tip = Column(Float, nullable=True)
  rounding_amount = Column(Float, nullable=True)
  discount = Column(Float, nullable=True)
  total_amount = Column(Float, nullable=False)
  receipt_url = Column(String, nullable=True)
  notes = Column(String, nullable=True)
  status = Column(
    Enum(ReceiptStatus),
    nullable=False,
    default=ReceiptStatus.processing,
    server_default="processing"
  )

  user_id = Column(
    UUID(as_uuid=True),
    ForeignKey("user.id", ondelete="CASCADE"),
    nullable=False,
    index=True
  )

  user = relationship("User", back_populates="receipts")
  participants = relationship("ReceiptParticipant", back_populates="receipt")
  items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")

class ReceiptParticipant(Base, Mixin):
  __tablename__ = "receipt_participant"

  id: Mapped[uuid4pk]
  is_owner = Column(
    nullable=False,
    default=False,
    server_default="false"
  )
  owes_amount = Column(Float, nullable=True)
  split_method = Column(
    Enum(SplitMethod), 
    nullable=False, 
    default=SplitMethod.weighted, 
    server_default="weighted"
  )

  receipt_id = Column(
    UUID(as_uuid=True),
    ForeignKey("receipt.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
  )

  participant_type = Column(Enum(ParticipantType), nullable=False)

  user_id = Column(
    UUID(as_uuid=True),
    ForeignKey("user.id", ondelete="CASCADE"),
    nullable=True,
    index=True,
  )

  external_contact_id = Column(
    UUID(as_uuid=True),
    ForeignKey("external_contact.id", ondelete="CASCADE"),
    nullable=True,
    index=True,
  )

  receipt = relationship("Receipt", back_populates="participants")
  user = relationship("User")
  external_contact = relationship("ExternalContact")

class ReceiptItem(Base, Mixin):
  __tablename__ = "receipt_item"

  id: Mapped[uuid4pk]
  name: Mapped[name]
  quantity = Column(Float, nullable=False)
  unit_price = Column(Float, nullable=False)
  total_price = Column(Float, nullable=False)

  receipt_id = Column(
    UUID(as_uuid=True),
    ForeignKey("receipt.id", ondelete="CASCADE"),
    index=True,
    nullable=False,
  )

  receipt = relationship("Receipt", back_populates="items")
  participants = relationship(
    "ReceiptItemFriend",
    back_populates="item",
    cascade="all, delete-orphan"
  )
  variations = relationship(
    "ReceiptItemVariation",
    back_populates="item",
    cascade="all, delete-orphan"
  )

class ReceiptItemFriend(Base, Mixin):
  __tablename__ = "receipt_item_friend"

  id: Mapped[uuid4pk]
  item_id = Column(UUID(as_uuid=True), ForeignKey("receipt_item.id", ondelete="CASCADE"), nullable=False, index=True)
  user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=True, index=True)
  external_contact_id = Column(UUID(as_uuid=True), ForeignKey("external_contact.id", ondelete="CASCADE"), nullable=True, index=True)
  share_ratio = Column(Float, nullable=True)

  item = relationship("ReceiptItem", back_populates="participants")
  user = relationship("User")
  external_contact = relationship("ExternalContact")

class ReceiptItemVariation(Base, Mixin):
  __tablename__ = "receipt_item_variation"

  id: Mapped[uuid4pk]
  name: Mapped[name]
  price = Column(Float, nullable=False)

  item_id = Column(
    UUID(as_uuid=True),
    ForeignKey("receipt_item.id", ondelete="CASCADE"),
    nullable=False,
    index=True
  )

  item = relationship("ReceiptItem", back_populates="variations")

