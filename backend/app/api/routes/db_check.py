from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.dependencies import get_db

router = APIRouter()

@router.get("/db-check")
def db_check(
    db: Session = Depends(get_db)
):
    db.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }