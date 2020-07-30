"""seo

Revision ID: c589aff75541
Revises: e803a86e4237
Create Date: 2020-07-30 10:32:08.970661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c589aff75541"
down_revision = "e803a86e4237"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "forj_contentnodecover", sa.Column("alt_text", sa.Text, nullable=True)
    )

    op.add_column(
        "forj_page", sa.Column("metadata_description", sa.Text, nullable=True)
    )
    op.add_column("forj_page", sa.Column("metadata_keywords", sa.Text, nullable=True))
    op.add_column("forj_page", sa.Column("metadata_author", sa.Text, nullable=True))


def downgrade():
    op.drop_column("forj_contentnodecover", "alt_text")
    op.drop_column("forj_page", "metadata_description")
    op.drop_column("forj_page", "metadata_author")
    op.drop_column("forj_page", "metadata_keywords")
