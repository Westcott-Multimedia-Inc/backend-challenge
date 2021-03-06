"""empty message

Revision ID: 17348cfdc5ba
Revises: 
Create Date: 2021-03-08 10:58:49.735729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17348cfdc5ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('artist_id', 'date', name='_artist_date_uc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('metric')
    op.drop_table('artist')
    # ### end Alembic commands ###
