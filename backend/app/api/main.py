from fastapi import APIRouter

from app.api.routes import auth_router, recognition_router

api_router = APIRouter()
api_router.include_router(auth_router.router)
api_router.include_router(recognition_router.router)
