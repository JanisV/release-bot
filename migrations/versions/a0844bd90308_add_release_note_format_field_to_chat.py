"""Add release_note_format field to Chat

Revision ID: a0844bd90308
Revises: 0f02a7a57103
Create Date: 2024-10-08 15:15:42.555006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0844bd90308'
down_revision = '0f02a7a57103'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('release_note_format', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.drop_column('release_note_format')

    # ### end Alembic commands ###
