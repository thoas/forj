from django.conf import settings

from django_hosts import reverse as reverse_full

from forj.payment.backends.base import Backend

import stripe


class StripeBackend(Backend):
    def handle_order(self, order, **kwargs):
        stripe_session = order.stripe_session

        if not stripe_session:
            cancel_url = reverse_full(
                "home", scheme=settings.DEFAULT_SCHEME, host=settings.DEFAULT_HOST,
            )

            success_url = order.get_payment_url()

            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "name": item["product"].name,
                        "description": item["product"].format_description(
                            item["reference"]
                        ),
                        "quantity": item["quantity"],
                        "currency": order.currency,
                        "amount": item["total"],
                    }
                    for item in order.get_items()
                ],
                locale=settings.STRIPE_LANGUAGE_CODE,
                customer_email=order.user.email,
                payment_method_types=["card"],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )

            order.stripe_session = session
            order.save(update_fields=("stripe_session",))

        stripe_session = order.stripe_session
        if stripe_session.payment_intent:
            payment_intent = stripe.PaymentIntent.retrieve(
                stripe_session.payment_intent
            )
            if payment_intent.status == "succeeded" and not order.is_status_succeeded():
                order.mark_as_succeeded()

        return order
