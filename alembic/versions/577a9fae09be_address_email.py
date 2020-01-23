"""address email

Revision ID: 577a9fae09be
Revises: ccd82f199f35
Create Date: 2020-01-23 22:46:30.046762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '577a9fae09be'
down_revision = 'ccd82f199f35'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "forj_address", sa.Column("email", sa.String(255), nullable=True)
    )

    op.alter_column("forj_order", "user_id", nullable=True)
    op.alter_column("forj_address", "user_id", nullable=True)


def downgrade():
    op.drop_column("forj_address", "email")

    op.alter_column("forj_order", "user_id", nullable=False)
    op.alter_column("forj_address", "user_id", nullable=False)
