""" Encapsulates online payments through stripe. """
# I've encapsulated these functions here to make it easier to change payment backend
# in future if necessary.

import stripe
import json

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template import loader
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.conf import settings

from events.models import Event, EventDate
from events.queries import get_remaining_event_dates

from .basket import (add_line_to_basket, update_line_in_basket, remove_line_from_basket,
                        remove_date_from_basket)

from .reports import generate_ticket_pdf
from .models import TicketType, Ticket, Order
from .forms import OrderForm
from .context import basket_contents
from .tickets import (check_basket_availability, check_order_availabillity,
                        Tickets_Not_Available)


def get_checkout_page(request):
    # Get the stripe secret and public keys
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Get the shopping basket
    basket = request.session.get('basket', {})
    if not basket:
        #TODO: add messaging
        return redirect(f'{reverse("events")}?type=show')

    # Are there still enough tickets for this order?
    try:
        check_basket_availability(basket)
    except Tickets_Not_Available as e:
        #TODO: add messaging
        # Remove problem lines from the basket
        remove_date_from_basket(e.date_id)
        return redirect(reverse('view_basket'))

    # Get the total cost
    total = basket_contents(request)['basket']['total']

    # Setup stripe
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    #TODO: Add profile get here
    order_form = OrderForm()


    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'boxoffice/checkout.html', context)


def precheckout_data(request):
    """ Accepts a request and attempts to cache precheckout data """
    try:
        check_basket_availability(basket)

        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_to_profile': request.POST.get('save_to_profile'),
            'username': request.user,
        })
        return HttpResponse(status=200)

    except Tickets_Not_Available as e:
        # TODO: django messaging goes here
        # Remove problem lines from the basket
        remove_date_from_basket(e.date_id)
        return HttpResponse(content=e, status=400)

    except Exception as e:
        # TODO: django messaging goes here
        return HttpResponse(content=e, status=400)


def complete_checkout(request):
    """ Receives checkout data after  """

    # Get the stripe secret and public keys
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Get the shopping basket
    basket = request.session.get('basket', {})
    if not basket:
        #TODO: django messaging goes here
        return redirect(f'{reverse("events")}?type=show')

    # Do we have all the information we need?
    if not set(['full_name','email','phone_number']).issubset(request.POST):
        #TODO: django messaging goes here
        return get_checkout_page(request)

    # Construct form object
    order_form = OrderForm({
        'full_name': request.POST['full_name'],
        'email': request.POST['email'],
        'phone_number': request.POST['phone_number'],
    })
    # If data is valid construct the order
    if order_form.is_valid():
        # Construct the order model
        order = order_form.save(commit=False)
        # Add the payment information to the order
        order.stripe_pid = request.POST.get('client_secret').split('_secret')[0]
        # Add the basket information to the order
        order.original_basket = json.dumps(basket)
        # Add the tickets to the order





# user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
#                                  null=True, blank=True, related_name='orders')










