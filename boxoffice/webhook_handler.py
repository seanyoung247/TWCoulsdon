""" Handles webhooks from payment backend """
import time
from django.http import HttpResponse
from .models import Order
from .reports import send_ticket_pdf_email
from .tickets import create_tickets_for_order


# Largely based on the boutique ado project
class StripeWHHandler:
    """ Handles stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded webhook from Stripe """

        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_to_profile = intent.metadata.save_to_profile

        billing_details = intent.charges.data[0].billing_details
        order_total = round(intent.charges.data[0].amount / 100, 2)

        # Update profile information if save_info was checked
        profile=None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    order_total=order_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            send_ticket_pdf_email(self.request, order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified \
                    order already in database', status=200)

        order = None
        try:
            order = Order.objects.create(
                full_name=billing_details.name,
                user_profile=profile,
                email=billing_details.email,
                phone_number=billing_details.phone,
                original_basket=basket,
                stripe_pid=pid,
            )
            create_tickets_for_order(order)
        except Exception as error:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {error}',
                status=500)

        send_ticket_pdf_email(self.request, order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)


    def handle_payment_intent_payment_failed(self, event):
        """ Handle the payment_intent.payment_failed webhook from Stripe """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
