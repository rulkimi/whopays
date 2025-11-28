"""add-status-to-receipt

Revision ID: 20251128_2200
Revises: 20251126_1721
Create Date: 2025-11-28 22:00:21.091972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251128_2200'
down_revision: Union[str, Sequence[str], None] = '20251126_1721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type for status
    status_enum = sa.Enum('processing', 'extracted', 'failed', name='receiptstatus')
    status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('receipt', sa.Column('status', status_enum, server_default='processing', nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('receipt', 'status')
    # Drop the enum type for status
    status_enum = sa.Enum('processing', 'extracted', 'failed', name='receiptstatus')
    status_enum.drop(op.get_bind(), checkfirst=True)
