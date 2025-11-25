"""add-friends-table-and-relation-with-user

Revision ID: 20251124_2117
Revises: 20251124_1639
Create Date: 2025-11-24 21:17:12.539490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '20251124_2117'
down_revision: Union[str, Sequence[str], None] = '20251124_1639'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	"""Upgrade schema."""
	# 1. Add username/photo_url column to user first (with username nullable for now, so we can ALTER it later)
	op.add_column('user', sa.Column('username', sa.String(length=30), nullable=True, unique=True))
	op.add_column('user', sa.Column('photo_url', sa.String(), nullable=True))
	# 2. Create index on user.username
	op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
	# 3. Now make username NOT NULL (only if you know data will be migrated in production before this step)
	op.alter_column('user', 'username', nullable=False)
	# 4. Create friend table (do NOT put index/unique=True on columns directly, handle with explicit op.create_index below)
	op.create_table(
		'friend',
		sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
		sa.Column('name', sa.String(length=30), nullable=False),
		sa.Column(
			'friend_user_id',
			UUID(as_uuid=True),
			sa.ForeignKey('user.id', ondelete='CASCADE'),
			nullable=False,
			unique=True
		),
		sa.Column('email', sa.String(), nullable=False),
		sa.Column('username', sa.String(length=30), nullable=False),
		sa.Column('photo_url', sa.String(), nullable=True),
		sa.Column('status', sa.String(length=16), nullable=False, server_default='pending'),
		sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
		sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
		sa.Column('is_deleted', sa.Boolean(), nullable=False),
		sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
	)
	# 5. Create indexes for friend explicitly (so they don't conflict)
	op.create_index(op.f('ix_friend_username'), 'friend', ['username'], unique=True)
	op.create_index(op.f('ix_friend_status'), 'friend', ['status'])
	op.create_index(op.f('ix_friend_email'), 'friend', ['email'], unique=True)
	op.create_index(op.f('ix_friend_friend_user_id'), 'friend', ['friend_user_id'])
	op.create_unique_constraint('uq_friend_friend_user_id', 'friend', ['friend_user_id'])
	# 6. Create user_friend association referencing friend.friend_user_id
	op.create_table(
		'user_friend',
		sa.Column('user_id', UUID(as_uuid=True), nullable=False),
		sa.Column('friend_id', UUID(as_uuid=True), nullable=False),
		sa.ForeignKeyConstraint(['friend_id'], ['friend.friend_user_id'], ),
		sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
		sa.PrimaryKeyConstraint('user_id', 'friend_id')
	)


def downgrade() -> None:
	"""Downgrade schema."""
	op.drop_table('user_friend')
	op.drop_index(op.f('ix_friend_friend_user_id'), table_name='friend')
	op.drop_index(op.f('ix_friend_status'), table_name='friend')
	op.drop_index(op.f('ix_friend_username'), table_name='friend')
	op.drop_index(op.f('ix_friend_email'), table_name='friend')
	op.drop_table('friend')
	op.drop_index(op.f('ix_user_username'), table_name='user')
	op.drop_column('user', 'photo_url')
	op.drop_column('user', 'username')
