"""add content column to posts table

Revision ID: 4fda398334c3
Revises: 093d79077090
Create Date: 2022-09-14 12:08:02.059417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fda398334c3'
down_revision = '093d79077090'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
