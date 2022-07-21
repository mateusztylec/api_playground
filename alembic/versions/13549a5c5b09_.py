"""create new column

Revision ID: 13549a5c5b09
Revises: 9e0b47e02b50
Create Date: 2022-07-21 20:35:54.533200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13549a5c5b09'
down_revision = '9e0b47e02b50'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",  sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
