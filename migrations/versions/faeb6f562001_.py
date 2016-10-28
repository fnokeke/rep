"""empty message

Revision ID: faeb6f562001
Revises: None
Create Date: 2016-10-27 15:22:40.674030

"""

# revision identifiers, used by Alembic.
revision = 'faeb6f562001'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('firstname', sa.String(length=120), nullable=True),
    sa.Column('lastname', sa.String(length=120), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('picture', sa.String(length=120), nullable=True),
    sa.Column('google_credentials', sa.String(length=2500), nullable=True),
    sa.Column('is_location_active', sa.Boolean(), nullable=True),
    sa.Column('is_mood_active', sa.Boolean(), nullable=True),
    sa.Column('is_sn_active', sa.Boolean(), nullable=True),
    sa.Column('moves_id', sa.String(length=120), nullable=True),
    sa.Column('moves_access_token', sa.String(length=120), nullable=True),
    sa.Column('moves_refresh_token', sa.String(length=120), nullable=True),
    sa.Column('rescuetime_access_token', sa.String(length=120), nullable=True),
    sa.Column('rescuetime_refresh_token', sa.String(length=120), nullable=True),
    sa.Column('pam_access_token', sa.String(length=120), nullable=True),
    sa.Column('pam_refresh_token', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_credentials'),
    sa.UniqueConstraint('moves_access_token'),
    sa.UniqueConstraint('moves_id'),
    sa.UniqueConstraint('moves_refresh_token'),
    sa.UniqueConstraint('pam_access_token'),
    sa.UniqueConstraint('pam_refresh_token'),
    sa.UniqueConstraint('rescuetime_access_token'),
    sa.UniqueConstraint('rescuetime_refresh_token')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###
