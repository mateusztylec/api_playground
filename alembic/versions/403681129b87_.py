"""add last few columns to posts table
Revision ID: 403681129b87
Revises: 65e10ddecc9d
Create Date: 2022-07-21 20:58:04.720102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '403681129b87'
down_revision = '65e10ddecc9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="published")
    op.drop_column(table_name="posts", column_name="created_at")
