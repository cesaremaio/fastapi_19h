"""CREATE TABLES users, posts

Revision ID: f8b9dcd8961f
Revises: 
Create Date: 2025-03-17 15:14:51.734560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8b9dcd8961f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False), 
        sa.Column("email", sa.Integer(), nullable=False, unique=True), 
        sa.Column("password", sa.Integer(), nullable=False), 
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )
    op.create_table(
        "posts", 
        sa.Column("id", sa.Integer(), nullable=False), 
        sa.Column("title", sa.String(), nullable=False), 
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("owner", sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    op.drop_table("posts")
    pass
