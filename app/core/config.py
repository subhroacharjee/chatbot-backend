from typing import Any

from fastapi import HTTPException


API_PREFIX = "/api/v1"
DATABASE_URI_ENV_KEY = "DATABASE_URL"
ASSISTANT_INSTRUCTION = (
    "You are a personal math tutor. Answer questions briefly, in a sentence or less."
)


def response(data: Any | None):
    return {
        "status": "ok",
        "data": data,
    }


def throw_error(error_code: int, message: str, error: Any | None = None):
    raise HTTPException(
        status_code=error_code,
        detail={
            "status": "error",
            "message": message,
            "error": error,
        },
    )
