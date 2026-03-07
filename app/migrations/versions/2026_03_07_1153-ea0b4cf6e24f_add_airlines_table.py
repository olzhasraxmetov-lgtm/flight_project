"""add airlines table

Revision ID: ea0b4cf6e24f
Revises: a050750619a0
Create Date: 2026-03-07 11:53:43.040249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ea0b4cf6e24f'
down_revision: Union[str, Sequence[str], None] = 'a050750619a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('airlines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('iata_code', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('iata_code'),
    sa.UniqueConstraint('name')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('airlines')
