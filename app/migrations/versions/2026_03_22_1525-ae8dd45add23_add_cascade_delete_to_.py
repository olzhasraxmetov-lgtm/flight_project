"""add_cascade_delete to SeatTemplateSeatsORM

Revision ID: ae8dd45add23
Revises: 6c261c57c54f
Create Date: 2026-03-22 15:25:29.618020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ae8dd45add23'
down_revision: Union[str, Sequence[str], None] = '6c261c57c54f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('seat_template_seats_seat_template_id_fkey'), 'seat_template_seats', type_='foreignkey')
    op.create_foreign_key(None, 'seat_template_seats', 'seat_templates', ['seat_template_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'seat_template_seats', type_='foreignkey')
    op.create_foreign_key(op.f('seat_template_seats_seat_template_id_fkey'), 'seat_template_seats', 'seat_templates', ['seat_template_id'], ['id'])
