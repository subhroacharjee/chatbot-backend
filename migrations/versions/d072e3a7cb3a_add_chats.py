"""add_chats

Revision ID: d072e3a7cb3a
Revises: 322c3abe4324
Create Date: 2024-08-18 17:17:28.724203

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.internal.chats.models import Chats


# revision identifiers, used by Alembic.
revision: str = "d072e3a7cb3a"
down_revision: Union[str, None] = "322c3abe4324"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
chat = Chats()


def upgrade() -> None:
    op.create_table(
        chat.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "session_id", sa.Integer, sa.ForeignKey("chat_sessions.id"), nullable=False
        ),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(True), nullable=False, default=sa.func.now()
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table(chat.__tablename__)
    pass
