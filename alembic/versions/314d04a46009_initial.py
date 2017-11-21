"""initial

Revision ID: 314d04a46009
Revises:
Create Date: 2017-07-15 20:10:14.338960

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import column


# revision identifiers, used by Alembic.
revision = '314d04a46009'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "forj_user",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('password', sa.String(128)),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_superuser', sa.Boolean),
        sa.Column('first_name', sa.String(30)),
        sa.Column('last_name', sa.String(150)),
        sa.Column('stripe_customer_id', sa.String(100), nullable=True),
        sa.Column('email', sa.String(254), unique=True),
        sa.Column('is_staff', sa.Boolean),
        sa.Column('is_active', sa.Boolean),
        sa.Column('date_joined', sa.DateTime(timezone=True)),
    )

    op.create_index('forj_user__email__idx', 'forj_user', ['email'])

    op.create_table(
        "forj_address",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.SmallInteger, nullable=False),
        sa.Column('status', sa.SmallInteger, nullable=False),
        sa.Column('first_name', sa.String(250), nullable=True),
        sa.Column('last_name', sa.String(250), nullable=True),
        sa.Column('business_name', sa.String(250), nullable=True),
        sa.Column('line1', sa.Text, nullable=True),
        sa.Column('line2', sa.Text, nullable=True),
        sa.Column('postal_code', sa.String(140), nullable=True),
        sa.Column('city', sa.String(140), nullable=True),
        sa.Column('country', sa.String(2), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('forj_user.id')),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index('forj_address__user_id__idx', 'forj_address', ['user_id'])

    op.create_table(
        "forj_product",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100)),
        sa.Column('reference', sa.String(100)),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('price', sa.Integer, nullable=True),
        sa.Column('formula', sa.String(100), nullable=True),
        sa.Column('currency', sa.String(3)),
        sa.Column('shipping_cost', sa.Integer),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index('forj_product__reference__idx', 'forj_product', ['reference'])

    op.create_table(
        "forj_order",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Integer),
        sa.Column('currency', sa.String(3)),
        sa.Column('reference', sa.String(30)),
        sa.Column('status', sa.SmallInteger, nullable=False),
        sa.Column('shipping_status', sa.SmallInteger, nullable=False),
        sa.Column('shipping_cost', sa.Integer, server_default="0"),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('forj_user.id')),
        sa.Column('shipping_address_id', sa.Integer, sa.ForeignKey('forj_address.id'), nullable=True),
        sa.Column('billing_address_id', sa.Integer, sa.ForeignKey('forj_address.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('stripe_card_id', sa.String(100), nullable=True),
        sa.Column('stripe_charge_id', sa.String(100), nullable=True),
    )

    op.create_index('forj_order__user_id__idx', 'forj_order', ['user_id'])

    op.create_table(
        "forj_orderitem",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('quantity', sa.Integer, server_default="0"),
        sa.Column('amount', sa.Integer),
        sa.Column('shipping_cost', sa.Integer, server_default="0"),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('forj_order.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('forj_product.id')),
        sa.Column('product_reference', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_index('forj_orderitem__product_id__idx', 'forj_orderitem', ['product_id'])

    op.create_table(
        "auth_group",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(80)),
    )

    op.create_index('auth_group__name__idx', 'auth_group', ['name'])

    op.create_table(
        "forj_user_groups",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('forj_user.id')),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('auth_group.id')),
    )

    op.create_unique_constraint('forj_user_groups__user_id__group_id__uniq', 'forj_user_groups', ['user_id', 'group_id'])

    op.create_table(
        "django_session",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('session_key', sa.String(40)),
        sa.Column('session_data', sa.Text),
        sa.Column('expire_date', sa.DateTime(timezone=True)),
    )

    op.create_unique_constraint('django_session__expire_date__idx', 'django_session', ['expire_date'])

    op.create_table(
        "django_content_type",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('app_label', sa.String(100)),
        sa.Column('model', sa.String(100)),
    )

    op.create_unique_constraint('django_content_type__app_label__model__uniq', 'django_content_type', ['app_label', 'model'])

    op.create_table(
        "auth_permission",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('content_type_id', sa.Integer, sa.ForeignKey('django_content_type.id')),
        sa.Column('codename', sa.String(100)),
    )

    op.create_unique_constraint('auth_permission__content_type_id__codename__uniq', 'auth_permission', ['content_type_id', 'codename'])
    op.create_index('auth_permission__content_type_id__idx', 'auth_permission', ['content_type_id'])

    op.create_table(
        "forj_user_user_permissions",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('forj_user.id')),
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('auth_permission.id')),
    )

    op.create_unique_constraint('forj_user_user_permissions__user_id__permission_id__uniq', 'forj_user_user_permissions', ['user_id', 'permission_id'])

    op.create_table(
        "auth_group_permissions",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('auth_group.id')),
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('auth_permission.id')),
    )

    op.create_unique_constraint('auth_group_permissions__group_id__permission_id__uniq', 'auth_group_permissions', ['group_id', 'permission_id'])
    op.create_index('auth_group_permissions__group_id__idx', 'auth_group_permissions', ['group_id'])
    op.create_index('auth_group_permissions__permission_id__idx', 'auth_group_permissions', ['permission_id'])

    op.create_table(
        "django_admin_log",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('action_time', sa.DateTime(timezone=True)),
        sa.Column('object_id', sa.Text, nullable=True),
        sa.Column('object_repr', sa.String(200)),
        sa.Column('action_flag', sa.SmallInteger),
        sa.Column('change_message', sa.Text),
        sa.Column('content_type_id', sa.Integer, sa.ForeignKey('django_content_type.id'), nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('forj_user.id')),
    )

    op.create_index('django_admin_log__content_type_id__idx', 'django_admin_log', ['content_type_id'])
    op.create_index('django_admin_log__user_id__idx', 'django_admin_log', ['user_id'])

    op.create_check_constraint(
        "django_admin_log_action_flag_check",
        "django_admin_log",
        column('action_flag') >= 0
    )

    op.create_table(
        "easy_thumbnails_source",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('storage_hash', sa.String(40)),
        sa.Column('name', sa.String(255)),
        sa.Column('modified', sa.DateTime(timezone=True)),
    )

    op.create_unique_constraint('easy_thumbnails_source__storage_hash__name__uniq', 'easy_thumbnails_source', ['storage_hash', 'name'])
    op.create_index('easy_thumbnails_source__name__idx', 'easy_thumbnails_source', ['name'])
    op.create_index('easy_thumbnails_source__storage_hash__idx', 'easy_thumbnails_source', ['storage_hash'])

    op.create_table(
        "easy_thumbnails_thumbnail",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('storage_hash', sa.String(40)),
        sa.Column('modified', sa.DateTime(timezone=True)),
        sa.Column('source_id', sa.Integer, sa.ForeignKey('easy_thumbnails_source.id')),
    )

    op.create_unique_constraint('easy_thumbnails_thumbnail__storage_hash__name__source_id__uniq', 'easy_thumbnails_thumbnail', ['storage_hash', 'name', 'source_id'])
    op.create_index('easy_thumbnails_thumbnail__name__idx', 'easy_thumbnails_thumbnail', ['name'])
    op.create_index('easy_thumbnails_thumbnail__storage_hash__idx', 'easy_thumbnails_thumbnail', ['storage_hash'])
    op.create_index('easy_thumbnails_thumbnail__source_id__idx', 'easy_thumbnails_thumbnail', ['source_id'])

    op.create_table(
        "easy_thumbnails_thumbnaildimensions",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('thumbnail_id', sa.Integer, sa.ForeignKey('easy_thumbnails_thumbnail.id')),
        sa.Column('width', sa.Integer),
        sa.Column('height', sa.Integer),
    )

    op.create_check_constraint(
        "easy_thumbnails_thumbnaildimensions__width_check",
        "easy_thumbnails_thumbnaildimensions",
        column('width') >= 0
    )

    op.create_check_constraint(
        "easy_thumbnails_thumbnaildimensions__height_check",
        "easy_thumbnails_thumbnaildimensions",
        column('height') >= 0
    )


def downgrade():
    pass
