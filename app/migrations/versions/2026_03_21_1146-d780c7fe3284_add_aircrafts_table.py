"""add aircrafts table

Revision ID: d780c7fe3284
Revises: b293b76d8ed5
Create Date: 2026-03-21 11:46:42.485511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd780c7fe3284'
down_revision: Union[str, Sequence[str], None] = 'b293b76d8ed5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('aircrafts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('manufacturer', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('aircrafts')
