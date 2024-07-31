"""add content column to posts table

Revision ID: 706953a01a60
Revises: 3a3b84f40e97
Create Date: 2024-07-31 16:44:32.044050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '706953a01a60'
down_revision: Union[str, None] = '3a3b84f40e97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
