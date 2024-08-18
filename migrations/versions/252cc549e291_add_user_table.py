"""add_user_table

Revision ID: 252cc549e291
Revises:
Create Date: 2024-08-18 12:13:44.484837

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "252cc549e291"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            autoincrement=True,
            nullable=False,
            index=True,
        ),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(True), nullable=False, default=sa.func.now),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
