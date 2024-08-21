"""create sets table

Revision ID: 711c4fa83f18
Revises: 7f4277537307
Create Date: 2024-08-21 02:51:19.781223

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Date, Enum, func, ForeignKey, DECIMAL


# revision identifiers, used by Alembic.
revision: str = '711c4fa83f18'
down_revision: Union[str, None] = '7f4277537307'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('sets',
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('reps_count', Integer),
                    Column('weight', DECIMAL(precision=3, scale=6)),
                    Column('set_number', Integer),
                    Column('notes', String(150), nullable=True),
                    Column('workout_exercise_id', Integer, ForeignKey('workout_exercises.id'), nullable=False),
                    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('sets')
