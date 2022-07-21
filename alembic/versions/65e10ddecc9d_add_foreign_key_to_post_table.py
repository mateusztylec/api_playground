"""add foreign-key to post table

Revision ID: 65e10ddecc9d
Revises: ba59ea3c9605
Create Date: 2022-07-21 20:53:11.233442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e10ddecc9d'
down_revision = 'ba59ea3c9605'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column(table_name="posts", column_name="owner_id")
