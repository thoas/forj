from forj.payment.backends.base import Backend
from forj.payment import exceptions

import stripe


class StripeBackend(Backend):
    def handle_user(self, user, **kwargs):
        if user.stripe_customer_id is None:
            user.stripe_customer = stripe.Customer.create(
                description="user:{}".format(user.pk)
            )
            user.save(update_fields=("stripe_customer",))

        return user

    def handle_order(self, order, **kwargs):
        try:
            if order.stripe_charge_id:
                charge = order.stripe_charge

                if charge.status == "succeeded" and not order.is_status_succeeded():
                    order.mark_as_succeeded()

                    return order

            self.handle_user(order.user)

            if "token" in kwargs:
                customer = order.user.stripe_customer
                card = customer.sources.create(source=kwargs["token"])
                order.stripe_card = card
                order.stripe_source = None
                order.save(update_fields=("stripe_card", "stripe_source"))
            else:
                card = order.stripe_card

            if card.status == "chargeable" and card.card.three_d_secure != "required":
                chargeable_source = card
            elif order.stripe_source_id:
                source = order.stripe_source

                if source.status == "pending":
                    if source.redirect.status == "pending":
                        order.redirect_url = source.redirect.url

                        return order
                    elif source.redirect.status == "failed":
                        order.stripe_source_id = None
                elif source.status == "chargeable":
                    chargeable_source = source

            if not order.stripe_source_id:
                source = stripe.Source.create(
                    amount=order.total,
                    currency=order.currency,
                    type="three_d_secure",
                    three_d_secure={"card": card},
                    redirect={"return_url": order.get_payment_processing_url()},
                )

                order.stripe_source = source
                order.save(update_fields=("stripe_source",))

                if source.status != "chargeable":
                    order.redirect_url = source.redirect.url

                    return order

                chargeable_source = source

            if chargeable_source:
                if (
                    not order.stripe_charge_id
                    or not order.stripe_charge.status != "succeeded"
                ):
                    charge = stripe.Charge.create(
                        amount=order.total,
                        currency=order.currency,
                        source=chargeable_source,
                        customer=order.user.stripe_customer_id,
                        description="order:{}".format(order.pk),
                        capture=True,
                    )

                    if charge.status == "succeeded":
                        order.mark_as_succeeded(commit=False)
                        order.stripe_charge = charge
                        order.save(update_fields=("status", "stripe_charge"))
        except stripe.CardError as e:
            raise exceptions.CardError("Invalid card") from e
        except stripe.StripeError as e:
            raise exceptions.PaymentError("Invalid payment") from e

        return order
