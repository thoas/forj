"""stripe session

Revision ID: ccd82f199f35
Revises: fde6881c4c4e
Create Date: 2020-01-23 21:06:23.469821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ccd82f199f35"
down_revision = "fde6881c4c4e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "forj_order", sa.Column("stripe_session_id", sa.String(100), nullable=True)
    )


def downgrade():
    op.drop_column("forj_order", "stripe_session_id")
