from django.contrib import admin  # noqa
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from forj.models import Order, Product, User, OrderItem


class UserAdmin(BaseUserAdmin):
    change_form_template = 'forj/admin/user/change_form.html'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('date_joined',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', '_price', '_shipping_cost')

    readonly_fields = (
        'currency', 'created_at', 'updated_at'
    )

    change_form_template = 'forj/admin/product/change_form.html'

    def _price(self, instance):
        return '{}{}'.format(
            instance.get_currency_display(),
            instance.price_converted)

    def _shipping_cost(self, instance):
        return '{}{}'.format(
            instance.get_currency_display(),
            instance.shipping_cost_converted)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

    fields = (
        'product',
        'product_reference',
        'quantity',
        'shipping_cost',
        'amount'
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', '_amount',
                    'status', 'user',
                    'created_at', 'updated_at')

    list_filter = ('status', 'shipping_status', 'created_at')

    readonly_fields = (
        'currency', 'created_at', 'updated_at'
    )

    inlines = (OrderItemInline, )

    fieldsets = (
        (None, {
            'fields': (
                'amount',
                'currency',
                'status',
                'user',
            ),
        }),
        ('Shipping', {
            'fields': (
                'shipping_cost',
                'shipping_status',
            )
        }),
        ('Information', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def _amount(self, instance):
        return '{}{}'.format(
            instance.get_currency_display(),
            instance.amount_converted)


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)

admin.site.site_title = 'Site admin'
admin.site.site_header = 'Forj administration'
