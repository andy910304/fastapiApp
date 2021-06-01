"""create post table

Revision ID: 4c952dfda39a
Revises: 4ad7c447edce
Create Date: 2021-05-31 14:54:22.975970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c952dfda39a'
down_revision = '4ad7c447edce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('title', sa.String(100)),
        sa.Column('body', sa.String(100)),
        sa.Column('owner_id', sa.Integer),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_date', sa.DateTime),
    )

    pass


def downgrade():
    pass
