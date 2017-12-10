"""Rename pageviews to pageview_count

Revision ID: ab2ed7a65f7c
Revises: 4ecd65e5e833
Create Date: 2017-12-10 01:31:16.216133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab2ed7a65f7c'
down_revision = '4ecd65e5e833'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('page', 'pageviews', new_column_name='view_count')
    pass
    # ### end Alembic commands ###


def downgrade():
    op.alter_column('page', 'view_count', new_column_name='pageviews')
    pass
    # ### end Alembic commands ###
