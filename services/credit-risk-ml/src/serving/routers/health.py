from fastapi import APIRouter

from src.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}