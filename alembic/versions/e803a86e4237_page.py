"""page

Revision ID: e803a86e4237
Revises: 577a9fae09be
Create Date: 2020-03-11 10:26:09.802713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e803a86e4237"
down_revision = "577a9fae09be"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "forj_page",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("button_label", sa.String(250), nullable=True),
        sa.Column("button_link", sa.String(250), nullable=True),
        sa.Column("cover", sa.String(250)),
        sa.Column("side_image", sa.String(250)),
        sa.Column('title', sa.String(250)),
        sa.Column('slug', sa.String(100)),
        sa.Column('subtitle', sa.Text, nullable=True),
        sa.Column("content", sa.Text),
        sa.Column("rank", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table("forj_page")
