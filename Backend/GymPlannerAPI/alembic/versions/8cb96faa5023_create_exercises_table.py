"""create user_exercises table

Revision ID: 8cb96faa5023
Revises: fc44fa4c2a45
Create Date: 2024-08-21 02:35:22.665500

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Date, Enum, func, ForeignKey


# revision identifiers, used by Alembic.
revision: str = '8cb96faa5023'
down_revision: Union[str, None] = 'fc44fa4c2a45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('exercises',
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('name', String(100)),
                    Column('target_muscle', String(100)),
                    Column('equipment', String(100), nullable=True),
                    Column('youtube_url', String(), nullable=True)
                    )


def downgrade() -> None:
    op.drop_table('exercises')
