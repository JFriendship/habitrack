from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health():
    return {
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG
    }
    # return {"status": "ok"}