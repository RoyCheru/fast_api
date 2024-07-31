"""add user table

Revision ID: 4283f4e8124b
Revises: 706953a01a60
Create Date: 2024-07-31 17:15:38.645456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4283f4e8124b'
down_revision: Union[str, None] = '706953a01a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),sa.Column('email',sa.String(), nullable=False),sa.Column('password',sa.String(), nullable=False),sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
