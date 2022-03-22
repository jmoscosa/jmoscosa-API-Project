"""add content column to posts table

Revision ID: 8b6decae604c
Revises: f5c1ae4c262a
Create Date: 2022-03-21 22:42:24.208910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b6decae604c'
down_revision = 'f5c1ae4c262a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(100), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
