"""create workouts table

Revision ID: fc44fa4c2a45
Revises: de2621bfa41c
Create Date: 2024-08-21 02:25:07.270495

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Date, Enum, func, ForeignKey
from src.models.training import TrainingType


# revision identifiers, used by Alembic.
revision: str = 'fc44fa4c2a45'
down_revision: Union[str, None] = 'de2621bfa41c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('workouts',
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('workout_date', Date, server_default=func.now()),
                    Column('type', Enum(TrainingType), nullable=True),
                    Column('notes', String(1000), nullable=True),
                    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
                    )



def downgrade() -> None:
    op.drop_table('workouts')
    op.execute('DROP TYPE IF EXISTS trainingtype')
