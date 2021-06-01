"""create user table

Revision ID: 4ad7c447edce
Revises: 
Create Date: 2021-05-28 16:20:20.891142

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ad7c447edce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('username', sa.String(100), unique=True),
        sa.Column('hashed_password', sa.String(100)),
        sa.Column('email', sa.String(200)),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_date', sa.DateTime),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    pass
