from fastapi import APIRouter, Depends
from app.core.responses import APIResponse
from app.modules.ai.service import AIService, get_ai_service

router = APIRouter()

@router.get("/health")
def get_ai_health_check(ai_service: AIService = Depends(get_ai_service)):
  response = ai_service.get_ai_health_check()
  return APIResponse.success(
    message="AI is healthy.",
    data=response
  )