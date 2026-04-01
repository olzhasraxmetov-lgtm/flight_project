"""add bookings table

Revision ID: 1294a1ad6765
Revises: 697f49b7d939
Create Date: 2026-04-01 11:52:54.789935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1294a1ad6765'
down_revision: Union[str, Sequence[str], None] = '697f49b7d939'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('booking_reference', sa.String(length=6), nullable=False),
    sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'CONFIRMED', 'CANCELLED', name='bookingstatus'), server_default='CREATED', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('booking_reference')
    )
    op.create_index(op.f('ix_bookings_user_id'), 'bookings', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_bookings_user_id'), table_name='bookings')
    op.drop_table('bookings')
