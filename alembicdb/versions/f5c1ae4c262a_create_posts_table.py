"""create posts table

Revision ID: f5c1ae4c262a
Revises: 
Create Date: 2022-03-21 22:31:42.331636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5c1ae4c262a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('Title', sa.Integer(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
