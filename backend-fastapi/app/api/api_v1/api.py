from fastapi import APIRouter
from app.api.api_v1.endpoints import chat, utils, login, users

api_router = APIRouter()

api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
