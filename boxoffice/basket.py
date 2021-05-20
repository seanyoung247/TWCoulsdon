""" Provides functions for dealing with the shopping basket """
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from events.models import Event, EventDate
from boxoffice.models import TicketType


def add_line_to_basket(request, date_id, type_id, quantity):
    basket = request.session.get('basket', {})

    if date_id in basket:
        if type_id in basket[date_id]:
            basket[date_id][type_id] += quantity
        else:
            basket[date_id][type_id] = quantity
    else:
        basket[date_id] = {type_id: quantity}

    print(basket)
    request.session['basket'] = basket