from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils.html import format_html

from forj.models import (
    Order,
    Product,
    User,
    OrderItem,
    ContentNode,
    ContentNodeCover,
    Page,
)
from forj.forms.fields import AmountField

from django_countries import countries


class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "rank", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    change_form_template = "forj/admin/page/change_form.html"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "subtitle",
                    "content",
                    "rank",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "metadata_author",
                    "metadata_keywords",
                    "metadata_description",
                ),
                "classes": ("collapse",)
            },
        ),
        (
            "Images",
            {
                "fields": (
                    "cover",
                    "side_image",
                )
            },
        ),
        (
            "Button",
            {
                "fields": (
                    "button_label",
                    "button_link",
                )
            },
        ),
    )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        return form

    def render_change_form(self, request, context, *args, **kwargs):
        res = super().render_change_form(request, context, *args, **kwargs)

        context['adminform'].form.fields['content'].widget.attrs['class'] += ' ckeditor'

        return res


admin.site.register(Page, PageAdmin)


class ContentNodeCoverInline(admin.StackedInline):
    model = ContentNodeCover
    extra = 1

    fields = ("image", "rank", "alt_text")


class ContentNodeAdmin(admin.ModelAdmin):
    list_display = ("subject", "type", "cover", "rank")
    list_filter = ("type",)

    inlines = (ContentNodeCoverInline,)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "type",
                    "title",
                    "description",
                    "legend",
                    "cover",
                    "product_reference",
                    "rank",
                )
            },
        ),
    )


admin.site.register(ContentNode, ContentNodeAdmin)


class UserAdmin(BaseUserAdmin):
    change_form_template = "forj/admin/user/change_form.html"

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("date_joined",)


class ProductAdminForm(forms.ModelForm):
    name = forms.CharField(required=True)
    reference = forms.CharField(required=True, widget=forms.Textarea)
    description = forms.CharField(required=False, widget=forms.Textarea)
    condition = forms.CharField(required=False, widget=forms.Textarea)
    formula = forms.CharField(required=False, widget=forms.Textarea)
    price = AmountField(required=False)
    tax_cost = AmountField(required=False)
    shipping_cost = AmountField(required=False)

    class Meta:
        model = Product
        fields = ()


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "reference",
        "_price",
        "condition",
        "_shipping_cost",
        "_tax_cost",
    )

    readonly_fields = ("currency", "created_at", "updated_at")

    change_form_template = "forj/admin/product/change_form.html"

    form = ProductAdminForm

    def _price(self, instance):
        if instance.price:
            return "{}{}".format(
                instance.get_currency_display(), instance.price_converted
            )

        return instance.formula

    def _shipping_cost(self, instance):
        return "{}{}".format(
            instance.get_currency_display(), instance.shipping_cost_converted
        )

    def _tax_cost(self, instance):
        return "{}{}".format(
            instance.get_currency_display(), instance.tax_cost_converted
        )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

    fields = ("product", "product_reference", "quantity", "shipping_cost", "amount")


class OrderAdminForm(forms.ModelForm):
    total = forms.CharField(required=False)
    shipping_first_name = forms.CharField(required=False)
    shipping_last_name = forms.CharField(required=False)
    shipping_email = forms.CharField(required=False)
    shipping_business_name = forms.CharField(required=False)
    shipping_line1 = forms.CharField(required=False, widget=forms.Textarea)
    shipping_line2 = forms.CharField(required=False, widget=forms.Textarea)
    shipping_postal_code = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_country = forms.ChoiceField(required=False, choices=countries)
    shipping_phone_number = forms.CharField(required=False)

    billing_first_name = forms.CharField(required=False)
    billing_last_name = forms.CharField(required=False)
    billing_email = forms.CharField(required=False)
    billing_business_name = forms.CharField(required=False)
    billing_line1 = forms.CharField(required=False, widget=forms.Textarea)
    billing_line2 = forms.CharField(required=False, widget=forms.Textarea)
    billing_postal_code = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)
    billing_country = forms.ChoiceField(required=False, choices=countries)
    billing_phone_number = forms.CharField(required=False)

    class Meta:
        model = Order
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderAdminForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields["total"].initial = self.instance.total_converted
            self.fields["total"].widget.attrs["disabled"] = True

            for field in ("shipping", "billing"):
                if getattr(self.instance, "%s_address_id" % field):
                    instance = getattr(self.instance, "%s_address" % field)

                    self.fields["%s_first_name" % field].initial = instance.first_name
                    self.fields["%s_last_name" % field].initial = instance.last_name
                    self.fields["%s_email" % field].initial = instance.email
                    self.fields[
                        "%s_business_name" % field
                    ].initial = instance.business_name
                    self.fields["%s_line1" % field].initial = instance.line1
                    self.fields["%s_line2" % field].initial = instance.line2
                    self.fields["%s_postal_code" % field].initial = instance.postal_code
                    self.fields["%s_city" % field].initial = instance.city
                    self.fields["%s_country" % field].initial = instance.country
                    self.fields[
                        "%s_phone_number" % field
                    ].initial = instance.phone_number


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "_amount",
        "_status",
        "shipping_status",
        "_user",
        "created_at",
        "updated_at",
    )

    list_filter = ("status", "shipping_status", "created_at")

    readonly_fields = ("currency", "created_at", "updated_at")

    change_form_template = "forj/admin/order/change_form.html"

    raw_id_fields = ("user",)

    inlines = (OrderItemInline,)

    form = OrderAdminForm

    fieldsets = (
        (None, {"fields": ("total", "amount", "currency", "status")}),
        ("Shipping", {"fields": ("shipping_cost", "shipping_status")}),
        (
            "Shipping address",
            {
                "fields": (
                    "shipping_first_name",
                    "shipping_last_name",
                    "shipping_email",
                    "shipping_business_name",
                    "shipping_line1",
                    "shipping_line2",
                    "shipping_city",
                    "shipping_postal_code",
                    "shipping_country",
                    "shipping_phone_number",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Billing address",
            {
                "fields": (
                    "billing_first_name",
                    "billing_last_name",
                    "billing_business_name",
                    "billing_line1",
                    "billing_line2",
                    "billing_city",
                    "billing_postal_code",
                    "billing_country",
                    "billing_phone_number",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Information", {"fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return Order.objects.prefetch_related("user", "shipping_address")

    def _user(self, instance):
        if instance.user_id:
            return instance.user.email

        if instance.shipping_address_id:
            return instance.shipping_address.email

        return ""

    def _status(self, instance):
        color = "blue"

        if instance.is_status_succeeded():
            color = "green"
        elif instance.is_status_failed():
            color = "green"

        return format_html(
            '<span style="color: {}">{}</span>'.format(
                color, instance.get_status_display()
            )
        )

    def _amount(self, instance):
        return "{}{}".format(instance.get_currency_display(), instance.total_converted)


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)

admin.site.site_title = "Site admin"
admin.site.site_header = "Forj administration"
