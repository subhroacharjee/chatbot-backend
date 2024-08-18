from sqlalchemy.orm import Session

from app.internal.auth.schemas import CurrentUser, User
from app.internal.chat_session import schema
from app.internal.chat_session.model import ChatSessions


def create_a_chat_session(
    db: Session,
    current_user: CurrentUser,
    chat_session: schema.ChatSessionBase | None = None,
):
    new_session = ChatSessions(user_id=current_user.id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return schema.ChatSession.model_validate(new_session)


def get_a_session(db: Session, user_id: int, session_id: int):
    return (
        db.query(ChatSessions)
        .filter((ChatSessions.id == session_id) & (ChatSessions.user_id == user_id))
        .first()
    )
