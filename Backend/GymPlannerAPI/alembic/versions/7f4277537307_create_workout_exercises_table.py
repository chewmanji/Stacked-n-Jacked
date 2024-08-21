"""create user_exercises table

Revision ID: 7f4277537307
Revises: 8cb96faa5023
Create Date: 2024-08-21 02:47:30.057536

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Date, Enum, func, ForeignKey


# revision identifiers, used by Alembic.
revision: str = '7f4277537307'
down_revision: Union[str, None] = '8cb96faa5023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('workout_exercises',
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('notes', String(300), nullable=True),
                    Column('workout_id', Integer, ForeignKey('workouts.id'), nullable=False),
                    Column('exercise_id', Integer, ForeignKey('exercises.id'), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('workout_exercises')
