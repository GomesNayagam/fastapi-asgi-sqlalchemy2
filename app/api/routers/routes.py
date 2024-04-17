from fastapi import APIRouter

from app.api.routers import heartbeat, user

api_router = APIRouter()


api_router.include_router(heartbeat.router, tags=["health"], prefix="/health")
api_router.include_router(user.router)
