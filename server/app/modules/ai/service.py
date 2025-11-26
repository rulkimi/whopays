from google import genai
from google.genai import types
from app.core.settings import settings
from app.dependencies.prompts import system_instruction
from app.modules.receipt.schema import ReceiptRead

class AIService:
	def __init__(self):
		if not settings.GEMINI_API_KEY:
			raise ValueError("GEMINI_API_KEY is not configured.")
		self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

	def get_ai_response(self, prompt: str, response_model=None, config_kwargs=None):
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
			contents=prompt,
			config=config
		)
		if response_model:
			return response_model.model_validate_json(response.text)
		return response.text

	def extract_receipt_data(self, prompt: str):
		return self.get_ai_response(
			prompt=prompt,
			response_model=ReceiptRead
		)

	def get_ai_health_check(self):
		try:
			ai_response = self.get_ai_response("How does AI work?")
		except Exception as e:
			raise RuntimeError(f"Failed to get AI response: {e}")
		return {"status": "ok", "ai_response": ai_response}

def get_ai_service():
	return AIService()
