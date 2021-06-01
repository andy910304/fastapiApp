"""create comment system

Revision ID: 8bfd8912c58d
Revises: 8b0a83c6d622
Create Date: 2021-06-01 13:03:16.987191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bfd8912c58d'
down_revision = '8b0a83c6d622'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('name', sa.String(100)),
        sa.Column('email', sa.String(1000)),
        sa.Column('body', sa.String(1000)),
        sa.Column('post_id', sa.Integer),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_date', sa.DateTime),
    )
    pass


def downgrade():
    pass
