"""empty message

Revision ID: 22691e779e3a
Revises: 184782f13fe7
Create Date: 2016-11-16 20:32:39.291771

"""

# revision identifiers, used by Alembic.
revision = '22691e779e3a'
down_revision = '184782f13fe7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mturk', sa.Column('access_token', sa.String(length=120), nullable=True))
    op.add_column('mturk', sa.Column('code', sa.String(length=120), nullable=True))
    op.add_column('mturk', sa.Column('moves_id', sa.String(length=120), nullable=True))
    op.add_column('mturk', sa.Column('refresh_token', sa.String(length=120), nullable=True))
    op.drop_column('mturk', u'w_access_token')
    op.drop_column('mturk', u'w_moves_id')
    op.drop_column('mturk', u'w_refresh_token')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mturk', sa.Column(u'w_refresh_token', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('mturk', sa.Column(u'w_moves_id', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('mturk', sa.Column(u'w_access_token', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('mturk', 'refresh_token')
    op.drop_column('mturk', 'moves_id')
    op.drop_column('mturk', 'code')
    op.drop_column('mturk', 'access_token')
    ### end Alembic commands ###