"""add_cascade_delete

Revision ID: 6c261c57c54f
Revises: 43ab254a5245
Create Date: 2026-03-22 15:21:37.626392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6c261c57c54f'
down_revision: Union[str, Sequence[str], None] = '43ab254a5245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('seat_templates_aircraft_model_id_fkey'), 'seat_templates', type_='foreignkey')
    op.create_foreign_key(None, 'seat_templates', 'aircrafts', ['aircraft_model_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'seat_templates', type_='foreignkey')
    op.create_foreign_key(op.f('seat_templates_aircraft_model_id_fkey'), 'seat_templates', 'aircrafts', ['aircraft_model_id'], ['id'])
