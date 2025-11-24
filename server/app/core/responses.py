from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

class APIResponse:
	@staticmethod
	def success(message: str = "", data: Optional[Dict[str, Any]] = None, code: Optional[int] = 200):
		content = {
			"success": True,
			"message": message,
			"data": jsonable_encoder(data or {}),
			"code": code
		}
		return JSONResponse(content=content, status_code=code or 200)

	@staticmethod
	def error(message: str = "", data: Optional[Dict[str, Any]] = None, code: Optional[int] = 400):
		content = {
			"success": False,
			"message": message,
			"data": jsonable_encoder(data or {}),
			"code": code
		}
		return JSONResponse(content=content, status_code=code or 400)
