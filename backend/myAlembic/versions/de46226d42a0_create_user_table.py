"""create user table

Revision ID: de46226d42a0
Revises: 
Create Date: 2025-04-15 22:05:04.852627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = 'de46226d42a0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user',
        sa.Column('username', sa.VARCHAR, primary_key=True),
        sa.Column('password', sa.VARCHAR, nullable=False),
        sa.Column('birthday', sa.Date),
        sa.Column('create_time', sa.DateTime, default=datetime.utcnow),
        # sa.Column('last_login', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user')
