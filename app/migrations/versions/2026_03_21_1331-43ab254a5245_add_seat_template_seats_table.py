"""add seat_template_seats table

Revision ID: 43ab254a5245
Revises: 3107f0164732
Create Date: 2026-03-21 13:31:29.118753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '43ab254a5245'
down_revision: Union[str, Sequence[str], None] = '3107f0164732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('seat_template_seats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seat_template_id', sa.Integer(), nullable=False),
    sa.Column('seat_number', sa.CHAR(length=4), nullable=False),
    sa.Column('cabin_class', sa.Enum('ECONOMY', 'BUSINESS', 'FIRST', name='cabinclass'), nullable=False),
    sa.Column('seat_type', sa.Enum('WINDOW', 'AISLE', 'MIDDLE', 'EXTRA_LEGROOM', name='seattype'), nullable=False),
    sa.ForeignKeyConstraint(['seat_template_id'], ['seat_templates.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('seat_template_id', 'seat_number', name='uq_st_seats_template_number')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('seat_template_seats')
