"""allow nullable friend_user_id

Revision ID: 20251125_1201
Revises: 20251124_2117
Create Date: 2025-11-25 12:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = "20251125_1201"
down_revision: Union[str, Sequence[str], None] = "20251124_2117"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.alter_column(
		"friend",
		"friend_user_id",
		existing_type=UUID(as_uuid=True),
		nullable=True
	)


def downgrade() -> None:
	op.alter_column(
		"friend",
		"friend_user_id",
		existing_type=UUID(as_uuid=True),
		nullable=False
	)

