"""email and phone number column addition

Revision ID: aa7dc3bbd5a3
Revises: f4182e0ce094
Create Date: 2024-12-26 15:32:26.169718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa7dc3bbd5a3'
down_revision: Union[str, None] = 'f4182e0ce094'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('query_users', sa.Column('email', sa.String(length=50), nullable=True))
    op.add_column('query_users', sa.Column('phone_number', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('query_users', sa.Column('timezone', sa.String(length=50), nullable=True))
    op.drop_column('query_users', sa.Column('timezone', sa.String(length=50), nullable=True))
