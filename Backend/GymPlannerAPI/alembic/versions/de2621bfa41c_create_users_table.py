"""create users table

Revision ID: de2621bfa41c
Revises: 
Create Date: 2024-08-21 02:02:04.328309

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, Integer, String, Date, Enum, func
from src.models.user import Gender

# revision identifiers, used by Alembic.
revision: str = 'de2621bfa41c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('email', String(150), unique=True, nullable=False),
                    Column('hashed_password', String),
                    Column('birth_date', Date, nullable=True),
                    Column('gender', Enum(Gender), default=Gender.Unknown),
                    Column('created_at', Date, server_default=func.now()),
                    Column('updated_at', Date, onupdate=func.now())
                    )


def downgrade() -> None:
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS gender')
