from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin

from forj.models import Order, Product, User


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', '_price', '_shipping_cost')

    readonly_fields = (
        'currency', 'created_at', 'updated_at'
    )

    def _price(self, instance):
        return '{}{}'.format(
            instance.get_currency_display(),
            instance.amount_converted)

    def _shipping_cost(self, instance):
        return '{}{}'.format(
            instance.get_currency_display(),
            instance.shipping_cost_converted)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', '_amount',
                    'status', 'user',
                    'created_at', 'updated_at')

    readonly_fields = (
        'currency', 'created_at', 'updated_at'
    )

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
