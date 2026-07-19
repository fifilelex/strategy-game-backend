"""initial schema

Revision ID: 24c47b7237e9
Revises: 
Create Date: 2026-07-19 10:49:45.565527

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "24c47b7237e9"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "gamestate",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(128), nullable=False),
        sa.Column("turn", sa.Integer, nullable=False),
        sa.Column("money", sa.Integer, nullable=False),
        sa.Column("income", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
    )

    op.create_table(
        "items",
        sa.Column("item_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("income", sa.Integer, nullable=False),
        sa.Column("cost", sa.Integer, nullable=False),
        sa.Column("description", sa.String(1024), nullable=False, default=""),
    )

    op.create_table(
        "ownership",
        sa.Column(
            "user_id", sa.Integer, sa.ForeignKey("gamestate.user_id"), primary_key=True
        ),
        sa.Column(
            "item_id", sa.Integer, sa.ForeignKey("items.item_id"), primary_key=True
        ),
    )


def downgrade() -> None:
    op.drop_table("ownership")
    op.drop_table("gamestate")
    op.drop_table("items")

    pass
