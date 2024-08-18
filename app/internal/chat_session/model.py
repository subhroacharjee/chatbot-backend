from sqlalchemy.orm import relationship
from app.core.db.database import Base
import sqlalchemy as sa
from app.internal.auth import model as auth_model


class ChatSessions(Base):
    __tablename__ = "chat_sessions"
    id = sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, index=True)
    user_id = sa.Column(
        "user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False
    )
    created_at = sa.Column(
        "created_at", sa.DateTime(True), nullable=False, default=sa.func.now()
    )

    users = relationship(auth_model.Users)
    pass
