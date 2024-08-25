"""remove_user_id_from_sets

Revision ID: 84586d52b5f9
Revises: 4339b15245a9
Create Date: 2024-08-25 21:33:43.603735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84586d52b5f9'
down_revision: Union[str, None] = '4339b15245a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('sets', 'user_id')


def downgrade() -> None:
    op.add_column('sets', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False))

