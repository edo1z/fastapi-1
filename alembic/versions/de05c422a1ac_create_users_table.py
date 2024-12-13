"""create users table

Revision ID: de05c422a1ac
Revises:
Create Date: 2024-12-13 10:48:01.319333

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de05c422a1ac"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
