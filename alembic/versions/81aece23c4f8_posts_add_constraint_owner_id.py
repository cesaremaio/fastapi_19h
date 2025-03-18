"""posts add constraint owner id

Revision ID: 81aece23c4f8
Revises: f8b9dcd8961f
Create Date: 2025-03-17 15:28:35.181125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81aece23c4f8'
down_revision: Union[str, None] = 'f8b9dcd8961f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # add primary key constraint for users.id
    op.create_primary_key("users_id_pk", "users", ["id"])


    op.create_foreign_key("post_users_fk", 
                          source_table="posts",
                          referent_table="users", 
                          local_cols=["owner_id"], 
                          remote_cols=["id"], 
                          ondelete="CASCADE"
                          )


    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_constraint("users_id_pk", "users", type_="primary")
    pass
