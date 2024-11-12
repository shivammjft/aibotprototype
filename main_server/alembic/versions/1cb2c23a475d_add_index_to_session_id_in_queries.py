"""Add index to session_id in Queries

Revision ID: 1cb2c23a475d
Revises: 
Create Date: 2024-11-12 12:13:57.173225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1cb2c23a475d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add index to session_id in the Queries table
    op.create_index(
        'ix_queries_session_id', 
        'queries',                 
        ['session_id'],          
        unique=False              
    )

def downgrade():
    # Drop the index if downgrading
    op.drop_index('ix_queries_session_id', table_name='queries')

