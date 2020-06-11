"""empty message

Revision ID: 17c69f1da9da
Revises: b6653c6db777
Create Date: 2020-06-10 13:34:12.511777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17c69f1da9da'
down_revision = 'b6653c6db777'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('mail', sa.String(length=100), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=True),
    sa.Column('contrasena', sa.String(length=20), nullable=False),
    sa.Column('telefono', sa.String(length=10), nullable=True),
    sa.Column('edad', sa.Integer(), nullable=True),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('trabajo', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('userID'),
    sa.UniqueConstraint('mail'),
    sa.UniqueConstraint('username')
    )
    op.create_table('evento',
    sa.Column('idEvento', sa.Integer(), nullable=False),
    sa.Column('Nombre', sa.String(length=100), nullable=False),
    sa.Column('Siglas', sa.String(length=30), nullable=False),
    sa.Column('Descripcion', sa.String(length=500), nullable=False),
    sa.Column('Duracion', sa.String(length=50), nullable=False),
    sa.Column('Cupo', sa.Integer(), nullable=False),
    sa.Column('Costo', sa.Integer(), nullable=False),
    sa.Column('Lugar', sa.String(length=100), nullable=False),
    sa.Column('Fecha', sa.DateTime(), nullable=False),
    sa.Column('imagen', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['usuario.userID'], ),
    sa.PrimaryKeyConstraint('idEvento')
    )
    op.create_table('boleto',
    sa.Column('folio', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('idEvento', sa.Integer(), nullable=True),
    sa.Column('Fecha', sa.DateTime(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=True),
    sa.Column('imagen', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['idEvento'], ['evento.idEvento'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usuario.userID'], ),
    sa.PrimaryKeyConstraint('folio')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('boleto')
    op.drop_table('evento')
    op.drop_table('usuario')
    # ### end Alembic commands ###
