"""add passengers table

Revision ID: e181ed360ecc
Revises: 1294a1ad6765
Create Date: 2026-04-01 11:54:55.985201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e181ed360ecc'
down_revision: Union[str, Sequence[str], None] = '1294a1ad6765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('passengers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('flight_instance_id', sa.Integer(), nullable=False),
    sa.Column('seat_instance_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('passport_number', sa.String(length=20), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], ),
    sa.ForeignKeyConstraint(['flight_instance_id'], ['flight_instances.id'], ),
    sa.ForeignKeyConstraint(['seat_instance_id'], ['seat_instances_map.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('seat_instance_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('passengers')
