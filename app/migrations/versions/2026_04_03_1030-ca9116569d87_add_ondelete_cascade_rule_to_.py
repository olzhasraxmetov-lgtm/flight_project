"""add ondelete=CASCADE rule to PassengersORM

Revision ID: ca9116569d87
Revises: e181ed360ecc
Create Date: 2026-04-03 10:30:15.007641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ca9116569d87'
down_revision: Union[str, Sequence[str], None] = 'e181ed360ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('passengers_booking_id_fkey'), 'passengers', type_='foreignkey')
    op.create_foreign_key(None, 'passengers', 'bookings', ['booking_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'passengers', type_='foreignkey') # type: ignore
    op.create_foreign_key(op.f('passengers_booking_id_fkey'), 'passengers', 'bookings', ['booking_id'], ['id'])