"""cms node cover

Revision ID: fde6881c4c4e
Revises: 7a62bf64609b
Create Date: 2018-03-04 22:52:12.400745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fde6881c4c4e"
down_revision = "7a62bf64609b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "forj_contentnodecover",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("image", sa.String(250), nullable=True),
        sa.Column("rank", sa.Integer, nullable=True),
        sa.Column("content_node_id", sa.Integer, sa.ForeignKey("forj_contentnode.id")),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table("forj_contentnodecover")
