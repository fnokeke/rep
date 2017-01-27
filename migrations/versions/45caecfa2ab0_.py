"""empty message

Revision ID: 45caecfa2ab0
Revises: 98a86a4c58dd
Create Date: 2016-12-13 07:10:58.186607

"""

# revision identifiers, used by Alembic.
revision = '45caecfa2ab0'
down_revision = '98a86a4c58dd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('intervention', sa.Column('code', sa.String(length=10), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('intervention', 'code')
    ### end Alembic commands ###