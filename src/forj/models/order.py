import shortuuid
import stripe

from django.db import models
from django.urls import reverse
from django.conf import settings

from mail_factory import factory

from forj import constants
from forj.db.models import base
from forj.db.models.fields import AmountField, ResourceField

from django_hosts import reverse as reverse_full

ORDER_SESSION_KEY = "cart_id"


class OrderManager(base.Manager):
    def from_request(self, request):
        result = request.session.get(ORDER_SESSION_KEY)
        if result is None:
            return None

        return self.filter(pk=result).first()

    def status_succeeded(self):
        return self.filter(status=self.model.STATUS_CHOICES.SUCCEEDED)


class Order(base.Model):
    STATUS_CHOICES = constants.ORDER_STATUS_CHOICES
    SHIPPING_STATUS_CHOICES = constants.ORDER_SHIPPING_STATUS_CHOICES

    amount = AmountField(verbose_name="Amount")
    currency = models.CharField(
        max_length=3,
        choices=constants.CURRENCY_CHOICES,
        default=constants.CURRENCY_CHOICES.EURO,
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=STATUS_CHOICES.WAITING
    )
    reference = models.CharField(max_length=30, verbose_name="Reference")
    shipping_status = models.PositiveSmallIntegerField(
        choices=SHIPPING_STATUS_CHOICES, default=SHIPPING_STATUS_CHOICES.WAITING
    )
    shipping_cost = AmountField(verbose_name="Shipping cost", default=0)
    tax_cost = AmountField(verbose_name="Tax cost", default=0)
    user = models.ForeignKey(
        "forj.User", on_delete=models.PROTECT, related_name="orders", null=True,
    )

    shipping_address = models.ForeignKey(
        "forj.Address",
        on_delete=models.SET_NULL,
        related_name="shipping_orders",
        null=True,
    )
    billing_address = models.ForeignKey(
        "forj.Address",
        on_delete=models.SET_NULL,
        related_name="billing_orders",
        null=True,
    )

    stripe_session = ResourceField(
        stripe.checkout.Session, null=True
    )

    objects = OrderManager()

    class Meta:
        abstract = False
        db_table = "forj_order"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.redirect_url = None

    def __str__(self):
        return "{} - {}{}/{}".format(
            self.reference,
            self.get_currency_display(),
            self.total_converted,
            self.get_status_display(),
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference = shortuuid.uuid()

        super().save(*args, **kwargs)

    def to_request(self, request):
        request.session[ORDER_SESSION_KEY] = self.pk

    @property
    def total(self):
        return self.amount + self.shipping_cost + self.tax_cost

    @property
    def total_converted(self):
        return round(self.total / 100.0, 2)

    def is_status_succeeded(self):
        return self.status == self.STATUS_CHOICES.SUCCEEDED

    def is_status_waiting(self):
        return self.status == self.STATUS_CHOICES.WAITING

    def is_status_failed(self):
        return self.status == self.STATUS_CHOICES.FAILED

    def get_payment_url(self):
        return reverse_full(
            "payment",
            args=[self.reference],
            scheme=settings.DEFAULT_SCHEME,
            host=settings.DEFAULT_HOST,
        )

    def get_success_url(self):
        return reverse("success", args=[self.reference])

    def get_invoice_url(self):
        return reverse_full(
            "invoice",
            args=[self.reference],
            scheme=settings.DEFAULT_SCHEME,
            host=settings.DEFAULT_HOST,
        )

    def get_checkout_url(self):
        return reverse("checkout", args=[self.reference])

    def mark_as_succeeded(self, commit=True, force=False):
        previous_status = self.status

        self.status = self.STATUS_CHOICES.SUCCEEDED

        if commit:
            self.save(update_fields=("status",))

        if previous_status != self.status or force is True:
            self.send_confirmation_mail()

    def send_confirmation_mail(self):
        factory.mail("confirmation", [self.shipping_address.email], {"order": self})

    @property
    def invoice_number(self):
        return Order.objects.status_succeeded().filter(id__lt=self.pk).count() + 1

    def get_items(self):
        products = []

        for item in self.items.select_related("product"):
            products.append(
                {
                    "quantity": item.quantity,
                    "reference": item.product_reference,
                    "product": item.product,
                    "total": item.total,
                }
            )

        return products


class OrderItem(base.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Quantity", default=1)
    product = models.ForeignKey(
        "forj.Product",
        related_name="items",
        verbose_name="Product",
        on_delete=models.CASCADE,
    )
    shipping_cost = AmountField(verbose_name="Shipping cost", default=0)
    tax_cost = AmountField(verbose_name="Tax cost", default=0)
    amount = AmountField(verbose_name="Total amount")
    product_reference = models.CharField(
        max_length=100, verbose_name="Product reference"
    )

    class Meta:
        abstract = False
        db_table = "forj_orderitem"

    @property
    def total(self):
        return self.amount + self.shipping_cost + self.tax_cost
