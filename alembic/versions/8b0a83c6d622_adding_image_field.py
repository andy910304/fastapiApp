"""adding image field

Revision ID: 8b0a83c6d622
Revises: 4c952dfda39a
Create Date: 2021-05-31 15:35:59.549501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b0a83c6d622'
down_revision = '4c952dfda39a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('url', sa.String(200))
    )


def downgrade():
    pass
