from google import genai
from google.genai import types
from app.core.settings import settings
from app.dependencies.prompts import system_instruction
from app.modules.receipt.schema import ReceiptRead

client = genai.Client(api_key=settings.GEMINI_API_KEY)
