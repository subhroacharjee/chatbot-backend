from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import assistant
from app.core.config import response
from app.core.db.database import get_db
from app.internal.auth.schemas import CurrentUser

from app.api import dependencies as dep
from app.internal.chat_session.session import create_a_chat_session
from app.internal.chats.chats import create_chat, delete_chat, update_chat
from app.internal.chats.openai_assistant import get_assistant
from app.internal.chats.schemas import ChatBase

chat_session_router = APIRouter(prefix="/session")


@chat_session_router.post("/")
def create_new_session(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(dep.get_current_user),
):
    return response(create_a_chat_session(db, current_user))


@chat_session_router.post(
    "/{session_id}/chat", dependencies=[Depends(dep.validate_chat_session_valid)]
)
def create_new_chat(
    session_id: int,
    data: ChatBase,
    db: Session = Depends(get_db),
    assistant: assistant.Assistant = Depends(get_assistant),
    current_user: CurrentUser = Depends(dep.get_current_user),
):
    return response(create_chat(db, assistant, session_id, current_user, data))


@chat_session_router.put(
    "/{session_id}/chat/{chat_id}",
    dependencies=[Depends(dep.validate_chat_session_valid)],
)
def update_old_chat(
    session_id: int,
    chat_id: int,
    data: ChatBase,
    db: Session = Depends(get_db),
    assistant: assistant.Assistant = Depends(get_assistant),
    current_user: CurrentUser = Depends(dep.get_current_user),
):
    return response(update_chat(db, assistant, chat_id, session_id, current_user, data))


@chat_session_router.delete(
    "/{session_id}/chat/{chat_id}",
    dependencies=[Depends(dep.validate_chat_session_valid)],
)
def delete_old_chat(
    session_id: int,
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(dep.get_current_user),
):
    return response(delete_chat(db, chat_id, session_id, current_user))
