"""add airports table

Revision ID: 1a6301b44a93
Revises: ea0b4cf6e24f
Create Date: 2026-03-09 12:14:31.492818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1a6301b44a93'
down_revision: Union[str, Sequence[str], None] = 'ea0b4cf6e24f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('airports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.CHAR(length=3), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.Column('timezone', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('airports')
