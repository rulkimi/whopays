from uuid import UUID
from fastapi import APIRouter, Depends, Body
from app.core.responses import APIResponse
from app.dependencies.auth import get_current_user
from app.modules.receipt.schema import (
	ReceiptCreate,
	ReceiptParticipantCreate,
	ReceiptItemCreate,
	ReceiptItemFriendCreate,
	ReceiptItemVariationCreate
)
from app.modules.receipt.service import ReceiptService, get_receipt_service

router = APIRouter()

@router.get("")
def get_receipts(
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	receipts = receipt_service.list(user_id=current_user.id)
	return APIResponse.success(
		message="Fetched receipts successfully.",
		data=receipts
	)

@router.get("/{receipt_id}")
def get_receipt(
	receipt_id: UUID,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	receipt = receipt_service.get(receipt_id=receipt_id)
	return APIResponse.success(
		message="Fetched receipt successfully.",
		data=receipt
	)

@router.post("")
def create_receipt(
	data: ReceiptCreate,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	if not getattr(data, "user_id", None):
		data.user_id = current_user.id
	created_receipt = receipt_service.create(data=data)
	return APIResponse.success(
		message="Receipt created successfully.",
		data=created_receipt
	)

@router.put("/{receipt_id}")
def edit_receipt(
	receipt_id: UUID,
	update_data: dict = Body(...),
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	updated_receipt = receipt_service.edit_receipt(receipt_id=receipt_id, update_data=update_data)
	return APIResponse.success(
		message="Receipt updated successfully.",
		data=updated_receipt
	)

@router.post("/{receipt_id}/participants")
def add_participant(
	receipt_id: UUID,
	data: ReceiptParticipantCreate,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	participant = receipt_service.add_participant(receipt_id=receipt_id, data=data)
	return APIResponse.success(
		message="Participant added successfully.",
		data=participant
	)

@router.post("/{receipt_id}/items")
def add_item(
	receipt_id: UUID,
	data: ReceiptItemCreate,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	item = receipt_service.add_item(receipt_id=receipt_id, data=data)
	return APIResponse.success(
		message="Item added successfully.",
		data=item
	)

@router.put("/items/{item_id}")
def edit_item(
	item_id: UUID,
	update_data: dict = Body(...),
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	updated_item = receipt_service.edit_item(item_id=item_id, update_data=update_data)
	return APIResponse.success(
		message="Item updated successfully.",
		data=updated_item
	)

@router.post("/items/{item_id}/participants")
def add_item_participant(
	item_id: UUID,
	data: ReceiptItemFriendCreate,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	friend = receipt_service.add_item_participant(item_id=item_id, data=data)
	return APIResponse.success(
		message="Item participant added successfully.",
		data=friend
	)

@router.post("/items/{item_id}/variations")
def add_item_variation(
	item_id: UUID,
	data: ReceiptItemVariationCreate,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	variation = receipt_service.add_item_variation(item_id=item_id, data=data)
	return APIResponse.success(
		message="Item variation added successfully.",
		data=variation
	)

@router.delete("/{receipt_id}")
def delete_receipt(
	receipt_id: UUID,
	receipt_service: ReceiptService = Depends(get_receipt_service),
	current_user=Depends(get_current_user),
):
	result = receipt_service.delete(receipt_id=receipt_id)
	return APIResponse.success(
		message=result.get("message", "Receipt deleted successfully."),
		data=None
	)
