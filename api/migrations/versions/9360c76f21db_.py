"""empty message

Revision ID: 9360c76f21db
Revises: 4893874fd3a5
Create Date: 2020-06-09 23:10:16.809329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9360c76f21db'
down_revision = '4893874fd3a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('date_posted', sa.DATETIME(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
