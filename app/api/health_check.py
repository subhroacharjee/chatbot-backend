from fastapi import APIRouter

from app.core.config import response


health_check_router = APIRouter(prefix="/health-check")


@health_check_router.get("/")
def health_check():
    return response(None)
