"""auto-vote

Revision ID: a72a79a1808b
Revises: 0fc44aa2ce7e
Create Date: 2022-09-14 22:51:43.840310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a72a79a1808b'
down_revision = '0fc44aa2ce7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.add_column('users', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'published')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    op.drop_table('votes')
    # ### end Alembic commands ###
