"""add page published type state

Revision ID: 45186df9ea98
Revises: 5a571e65a995
Create Date: 2017-12-07 16:04:51.204013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45186df9ea98'
down_revision = '5a571e65a995'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pagestate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('page', sa.Column('pagestate_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_page_pagestate', 'page', 'pagestate', ['pagestate_id'], ['id'])

    op.execute("INSERT INTO pagestate(title) values('Draft')")
    op.execute("INSERT INTO pagestate(title) values('Published')")

    conn = op.get_bind()
    res = conn.execute("select id from pagestate where title='Published'")
    results = res.fetchone()
    id = results[0]

    op.execute("update page set pagestate_id={}".format(id))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_page_pagestate', 'page', type_='foreignkey')
    op.drop_column('page', 'pagestate_id')
    op.drop_table('pagestate')
    # ### end Alembic commands ###