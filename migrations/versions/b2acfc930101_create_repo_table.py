"""Create Repo table

Revision ID: b2acfc930101
Revises: 7f96fae84d5f
Create Date: 2024-09-26 12:41:52.270977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2acfc930101'
down_revision = '7f96fae84d5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('current_tag', sa.String(), nullable=True),
    sa.Column('current_release_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repo')
    # ### end Alembic commands ###
