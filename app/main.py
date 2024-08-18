from fastapi import APIRouter
from app.api import chat_session, health_check, user
from app.core.config import API_PREFIX
from app.core.setup import create_application

api_router = APIRouter(prefix=API_PREFIX)
api_router.include_router(health_check.health_check_router)
api_router.include_router(user.user_router)
api_router.include_router(chat_session.chat_session_router)

app = create_application(api_router)
