from fastapi import APIRouter
from .health import router as health_router
from .db_check import router as db_check_router
from .auth import router as auth_router
from .habits import router as habit_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(db_check_router, tags=["DB_Check"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(habit_router, tags=["habits"])