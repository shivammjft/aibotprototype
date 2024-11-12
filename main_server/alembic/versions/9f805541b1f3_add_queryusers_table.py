"""Add QueryUsers table

Revision ID: 9f805541b1f3
Revises: 1cb2c23a475d
Create Date: 2024-11-12 12:16:52.982234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9f805541b1f3'
down_revision: Union[str, None] = '1cb2c23a475d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'query_users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('session_id', sa.String(255), sa.ForeignKey("queries.session_id")),
        sa.Column('chatbot_id', sa.String(255), sa.ForeignKey("chatbots.chatbot_id")),
        sa.Column('country', sa.String(100), nullable=True, index=True),
        sa.Column('ip_address', sa.String(100)),
        sa.Column('origin_url', sa.String(255)),
    )

def downgrade():
    op.drop_table('query_users')