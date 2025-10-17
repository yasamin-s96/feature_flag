from fastapi import APIRouter

from .routers.feature_flag import router as feature_flag_router

router = APIRouter(prefix="/api")

router.include_router(feature_flag_router)