"""Add session user  information fields to QueryUsers

Revision ID: 43317d9b3ce0
Revises: 9f805541b1f3
Create Date: 2024-11-12 16:15:26.132320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43317d9b3ce0'
down_revision: Union[str, None] = '9f805541b1f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Adding new columns to query_users table
    op.add_column('query_users', sa.Column('timezone', sa.String(length=50), nullable=True))
    op.add_column('query_users', sa.Column('language', sa.String(length=10), nullable=True))
    op.add_column('query_users', sa.Column('is_mobile', sa.Boolean(), nullable=True))
    op.add_column('query_users', sa.Column('user_agent', sa.Text(), nullable=True))
    op.add_column('query_users', sa.Column('platform', sa.String(length=255), nullable=True))
    op.add_column('query_users', sa.Column('referrer', sa.String(length=255), nullable=True))
    op.add_column('query_users', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('query_users', sa.Column('network_type', sa.String(length=50), nullable=True))

def downgrade():
    # Dropping columns from query_users table
    op.drop_column('query_users', 'timezone')
    op.drop_column('query_users', 'language')
    op.drop_column('query_users', 'is_mobile')
    op.drop_column('query_users', 'user_agent')
    op.drop_column('query_users', 'platform')
    op.drop_column('query_users', 'referrer')
    op.drop_column('query_users', 'location')
    op.drop_column('query_users', 'network_type')

