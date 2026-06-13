from fastapi import APIRouter, Depends
from app.core.config import settings
from app.db.dependencies import get_db

router = APIRouter()

@router.get("/health")
def health():
    return {
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG
    }
    # return {"status": "ok"}

@router.get("/db_health")
def db_health(db = Depends(get_db)):
    return {"status": "ok"}
