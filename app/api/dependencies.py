from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import API_PREFIX, throw_error
from app.core.db.database import get_db
from app.core.security import decode_access_token
from app.internal.auth import schemas
from app.internal.auth.auth import get_user
from app.internal.chat_session.session import get_a_session

oauth2 = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2)], db: Annotated[Session, Depends(get_db)]
):
    try:
        payload = decode_access_token(token)
        user = schemas.CurrentUser.model_validate(payload)
        if get_user(db, user.username):
            return user
    except Exception as e:
        print("[ERROR]", e)
        pass
    return throw_error(401, "invalid access token")


async def validate_chat_session_valid(
    current_user: Annotated[schemas.CurrentUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    session_id: int,
):
    try:
        session = get_a_session(db, current_user.id, session_id)
        if session is None:
            throw_error(404, "not found session")
    except Exception as e:
        print("[ERROR]", e)
        throw_error(404, "not found session")
