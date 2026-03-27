"""add seat_instances_map table

Revision ID: 697f49b7d939
Revises: 4d43848dcc78
Create Date: 2026-03-26 14:35:17.846363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

revision: str = '697f49b7d939'
down_revision: Union[str, Sequence[str], None] = '4d43848dcc78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('seat_instances_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_instance_id', sa.Integer(), nullable=False),
    sa.Column('seat_number', sa.String(length=5), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('seat_letter', sa.String(length=1), nullable=False),
    sa.Column('cabin_class',
              postgresql.ENUM('ECONOMY', 'BUSINESS', 'FIRST', name='cabinclass', create_type=False),
              nullable=False),
    sa.Column('seat_type',
              postgresql.ENUM('WINDOW', 'AISLE', 'MIDDLE', 'EXTRA_LEGROOM', name='seattype',
                              create_type=False), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'RESERVED', 'SOLD', 'BLOCKED', 'CHECKED_IN', name='seatstatus'), nullable=False),
    sa.Column('price_override', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['flight_instance_id'], ['flight_instances.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flight_instance_id', 'seat_number', name='uq_flight_seat')
    )
    op.create_index(op.f('ix_seat_instances_map_flight_instance_id'), 'seat_instances_map', ['flight_instance_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_seat_instances_map_flight_instance_id'), table_name='seat_instances_map')
    op.drop_table('seat_instances_map')
