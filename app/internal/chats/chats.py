from sqlalchemy.orm import Session

from app.core.assistant import Assistant
from app.core.config import throw_error
from app.internal.auth.schemas import CurrentUser
from app.internal.chats.models import Chats
from app.internal.chats.schemas import Chat, ChatBase


def create_chat(
    db: Session,
    assistant: Assistant,
    session_id: int,
    current_user: CurrentUser,
    prompt: ChatBase,
):
    reply = assistant.get_response_for_prompt(prompt.prompt)
    new_chat = Chats(
        prompt=prompt.prompt,
        response=reply.strip(),
        user_id=current_user.id,
        session_id=session_id,
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return Chat.model_validate(new_chat, strict=False)


def update_chat(
    db: Session,
    assistant: Assistant,
    id: int,
    session_id: int,
    current_user: CurrentUser,
    prompt: ChatBase,
):
    old_chat = (
        db.query(Chats)
        .filter(
            (Chats.id == id)
            & (Chats.session_id == session_id)
            & (Chats.user_id == current_user.id)
        )
        .first()
    )
    if old_chat is None:
        return throw_error(404, "chat not found")

    reply = assistant.get_response_for_prompt(prompt.prompt)
    old_chat.prompt = prompt.prompt  # type: ignore
    old_chat.response = reply  # type: ignore

    db.commit()

    db.refresh(old_chat)
    return Chat.model_validate(old_chat)


def delete_chat(
    db: Session,
    id: int,
    session_id: int,
    current_user: CurrentUser,
):
    del_count = (
        db.query(Chats)
        .filter(
            (Chats.id == id)
            & (Chats.session_id == session_id)
            & (Chats.user_id == current_user.id)
        )
        .delete()
    )
    if del_count is None or del_count == 0:
        return throw_error(404, "chat not found")

    db.commit()
    return
