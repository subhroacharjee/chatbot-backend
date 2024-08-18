"""add_chat_session

Revision ID: 322c3abe4324
Revises: 252cc549e291
Create Date: 2024-08-18 14:59:16.490602

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.internal.chat_session.model import ChatSessions


# revision identifiers, used by Alembic.
revision: str = "322c3abe4324"
down_revision: Union[str, None] = "252cc549e291"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ses = ChatSessions()


def upgrade() -> None:
    op.create_table(
        ses.__tablename__,
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(True), nullable=False, default=sa.func.now()
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table(ses.__tablename__)
    pass
