from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

class APIResponse:
	@staticmethod
	def success(message: str = "", data: Optional[Dict[str, Any]] = None, code: Optional[int] = 200):
		content = {
			"success": True,
			"message": message,
			"data": jsonable_encoder(data or None),
			"code": code
		}
		return JSONResponse(content=content, status_code=code or 200)

	@staticmethod
	def error(
		message: str = "",
		data: Optional[Dict[str, Any]] = None,
		errors: Optional[Dict[str, Any]] = None,
		code: Optional[int] = 400
	):
		content = {
			"success": False,
			"message": message,
			"data": jsonable_encoder(data or None),
			"errors": jsonable_encoder(errors or None),
			"code": code
		}
		return JSONResponse(content=content, status_code=code or 400)

class AppException(Exception):
  def __init__(self, message: str = "", code: int = 400, data=None, errors: Optional[dict] = None):
    self.message = message
    self.code = code
    self.data = data
    self.errors = errors
