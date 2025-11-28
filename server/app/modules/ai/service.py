from typing import Optional
from uuid import UUID
from fastapi import UploadFile
from google import genai
from google.genai import types
from app.core.settings import settings
from app.modules.ai.prompts import system_instruction, receipt_extraction_prompt
from app.modules.receipt.schema import ReceiptAIExtracted
from app.modules.receipt.service import ReceiptService

class AIService:
	def __init__(self):
		if not settings.GEMINI_API_KEY:
			raise ValueError("GEMINI_API_KEY is not configured.")
		self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

	def _normalize_contents(self, contents):
		if isinstance(contents, str):
			return [types.Content(role="user", parts=[types.Part.from_text(text=contents)])]
		return contents

	def get_ai_response(self, contents, response_model=None, config_kwargs=None):
		config = types.GenerateContentConfig(
			thinking_config=types.ThinkingConfig(thinking_budget=0),
			system_instruction=system_instruction,
		)
		if response_model:
			config.response_mime_type = "application/json"
			config.response_json_schema = response_model.model_json_schema()
		if config_kwargs:
			for k, v in config_kwargs.items():
				setattr(config, k, v)

		response = self.client.models.generate_content(
			model="gemini-2.5-flash",
			contents=self._normalize_contents(contents),
			config=config
		)
		if response_model:
			return response_model.model_validate_json(response.text)
		return response.text

	async def extract_receipt_data(self, receipt_image: UploadFile, prompt: str = receipt_extraction_prompt):
		receipt_image_bytes = await receipt_image.read()
		user_content = types.Content(
			role="user",
			parts=[
				types.Part.from_text(text=prompt),
				types.Part.from_bytes(
					data=receipt_image_bytes,
					mime_type=receipt_image.content_type or "image/jpeg"
				)
			]
		)
		return self.get_ai_response(
			contents=[user_content],
			response_model=ReceiptAIExtracted
		)

	async def extract_and_store_receipt(
		self,
		receipt_image: UploadFile,
		user_id: UUID,
		receipt_service: ReceiptService,
		prompt: str = receipt_extraction_prompt,
		receipt_url: Optional[str] = None
	):
		"""
		Extracts receipt data via AI and persists the structured output as a
		receipt tied to the requesting user.
		"""
		extracted = await self.extract_receipt_data(
			receipt_image=receipt_image,
			prompt=prompt
		)
		if receipt_url and not extracted.receipt_url:
			extracted = extracted.model_copy(update={"receipt_url": receipt_url})
		return receipt_service.create_from_ai_extract(
			user_id=user_id,
			extracted=extracted
		)

	def get_ai_health_check(self):
		try:
			ai_response = self.get_ai_response("How does AI work?")
		except Exception as e:
			raise RuntimeError(f"Failed to get AI response: {e}")
		return {"status": "ok", "ai_response": ai_response}


def get_ai_service():
	return AIService()
