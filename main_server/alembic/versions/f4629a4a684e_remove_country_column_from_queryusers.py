"""Remove country column from QueryUsers

Revision ID: f4629a4a684e
Revises: 43317d9b3ce0
Create Date: 2024-11-12 16:34:00.336836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f4629a4a684e'
down_revision: Union[str, None] = '43317d9b3ce0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Remove the 'country' column from 'query_users'
    op.drop_column('query_users', 'country')


def downgrade():
    # Re-add the 'country' column to 'query_users' (for downgrade/rollback)
    op.add_column('query_users', sa.Column('country', sa.String(length=100), nullable=True))