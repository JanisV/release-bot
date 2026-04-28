"""Add release_notification table

Revision ID: b5e2d8f1c0f4
Revises: 6c2a7c346237
Create Date: 2026-04-28 19:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5e2d8f1c0f4'
down_revision = '6c2a7c346237'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'release_notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chat_id', sa.Integer(), nullable=True),
        sa.Column('repo_id', sa.Integer(), nullable=True),
        sa.Column('release_id', sa.Integer(), nullable=True),
        sa.Column('release_tag', sa.String(), nullable=True),
        sa.Column('release_title', sa.String(), nullable=True),
        sa.Column('release_url', sa.String(), nullable=True),
        sa.Column('release_body', sa.Text(), nullable=True),
        sa.Column('repo_full_name', sa.String(), nullable=True),
        sa.Column('repo_link', sa.String(), nullable=True),
        sa.Column('pre_release', sa.Boolean(), nullable=True),
        sa.Column('updated', sa.Boolean(), nullable=True),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('summarized_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
        sa.ForeignKeyConstraint(['repo_id'], ['repo.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_release_notification_chat_id', 'release_notification', ['chat_id'], unique=False)
    op.create_index('ix_release_notification_sent_at', 'release_notification', ['sent_at'], unique=False)
    op.create_index('ix_release_notification_summarized_at', 'release_notification', ['summarized_at'], unique=False)



def downgrade():
    op.drop_index('ix_release_notification_summarized_at', table_name='release_notification')
    op.drop_index('ix_release_notification_sent_at', table_name='release_notification')
    op.drop_index('ix_release_notification_chat_id', table_name='release_notification')
    op.drop_table('release_notification')
