"""remove_user_id_from_workout_exercise

Revision ID: 4339b15245a9
Revises: 711c4fa83f18
Create Date: 2024-08-25 21:26:26.921674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4339b15245a9'
down_revision: Union[str, None] = '711c4fa83f18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('workout_exercises', 'user_id')


def downgrade() -> None:
    op.add_column('workout_exercises', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False))
