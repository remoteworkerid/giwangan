"""Add description for site

Revision ID: 02a04bf8bd66
Revises: 45186df9ea98
Create Date: 2017-12-07 22:57:58.823306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02a04bf8bd66'
down_revision = '45186df9ea98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('siteconfiguration', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('siteconfiguration', 'description')
    # ### end Alembic commands ###