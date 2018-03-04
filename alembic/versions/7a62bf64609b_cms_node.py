"""cms node

Revision ID: 7a62bf64609b
Revises: 314d04a46009
Create Date: 2018-03-04 21:50:19.778839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a62bf64609b'
down_revision = '314d04a46009'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "forj_contentnode",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(250), nullable=True),
        sa.Column('type', sa.String(20)),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('legend', sa.String(250), nullable=True),
        sa.Column('cover', sa.String(250), nullable=True),
        sa.Column('product_reference', sa.String(100), nullable=True),
        sa.Column('rank', sa.Integer, nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index('forj_contentnode__type__idx', 'forj_contentnode', ['type'])


def downgrade():
    op.drop_table('forj_contentnode')
