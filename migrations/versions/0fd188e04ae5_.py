"""empty message

Revision ID: 0fd188e04ae5
Revises: 16ade1c22ea3
Create Date: 2016-04-24 11:52:54.282000

"""

# revision identifiers, used by Alembic.
revision = '0fd188e04ae5'
down_revision = '16ade1c22ea3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fooditem', sa.Column('veg', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fooditem', 'veg')
    ### end Alembic commands ###
