"""empty message

Revision ID: 2c8d4f3b84f5
Revises: 22691e779e3a
Create Date: 2016-11-17 14:16:04.238325

"""

# revision identifiers, used by Alembic.
revision = '2c8d4f3b84f5'
down_revision = '22691e779e3a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mturk', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('mturk', sa.Column('ip', sa.String(length=24), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mturk', 'ip')
    op.drop_column('mturk', 'created_at')
    ### end Alembic commands ###