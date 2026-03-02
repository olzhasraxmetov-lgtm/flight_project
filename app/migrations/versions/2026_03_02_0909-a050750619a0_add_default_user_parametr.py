"""add default user parametr

Revision ID: a050750619a0
Revises: 5bcfabf8c07f
Create Date: 2026-03-02 09:09:47.534187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a050750619a0'
down_revision: Union[str, Sequence[str], None] = '5bcfabf8c07f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'role', server_default='user')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'role', server_default=None)
    pass
