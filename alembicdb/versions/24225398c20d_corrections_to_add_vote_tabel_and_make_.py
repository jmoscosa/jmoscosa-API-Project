"""Corrections to add Vote tabel and make a new title_of_Post column

Revision ID: 24225398c20d
Revises: 622c68f0c031
Create Date: 2022-03-22 16:51:34.886326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '24225398c20d'
down_revision = '622c68f0c031'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title_of_post', sa.String(length=20), nullable=False))
    op.drop_column('posts', 'Title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('Title', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('posts', 'title_of_post')
    # ### end Alembic commands ###