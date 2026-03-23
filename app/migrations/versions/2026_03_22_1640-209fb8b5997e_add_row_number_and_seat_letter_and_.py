"""add row_number and seat_letter and indexes for them

Revision ID: 209fb8b5997e
Revises: ae8dd45add23
Create Date: 2026-03-22 16:40:05.048395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '209fb8b5997e'
down_revision: Union[str, Sequence[str], None] = 'ae8dd45add23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('seat_template_seats', sa.Column('row_number', sa.Integer(), nullable=False))
    op.add_column('seat_template_seats', sa.Column('seat_letter', sa.CHAR(length=1), nullable=False))
    op.create_index('ix_st_seats_template_row_letter', 'seat_template_seats', ['seat_template_id', 'row_number', 'seat_letter'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_st_seats_template_row_letter', table_name='seat_template_seats')
    op.drop_column('seat_template_seats', 'seat_letter')
    op.drop_column('seat_template_seats', 'row_number')
