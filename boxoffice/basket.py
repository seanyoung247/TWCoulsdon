""" Provides functions for dealing with the shopping basket """

from events.models import EventDate
from .models import TicketType
from .tickets import check_ticket_available, TicketsNotAvailable


def get_ticket_lines_from_basket(basket):
    """
    Formats a basket into a ticket line item list

    Parameters:
    basket (shopping basket): The basket in the format stored in request

    Return:
    A line item style format with the appropriate database objects

    Usage:
    order_basket = get_ticket_lines_from_basket(request.session.get('basket', {}))

    """
    if basket:
        order_basket = []
        for date_id in basket:
            # If the eventdate isn't in the database move to next item
            # (I want to fail silently here, just drop anything unavailable)
            try:
                event_date = EventDate.objects.get(id=date_id)
            except EventDate.DoesNotExist:
                continue
            for type_id in basket[date_id]:
                try:
                    ticket_type = TicketType.objects.get(id=type_id)
                except TicketType.DoesNotExist:
                    continue
                order_basket.append({
                    'date': event_date,
                    'type': ticket_type,
                    'quantity': basket[date_id][type_id],
                })
        return order_basket

    return []


def _get_total_for_date(basket, date_id):
    """ Gets the total quantity in the basket for a given date """
    total = 0
    for type_id in basket[date_id]:
        total += basket[date_id][type_id]

    return total


def add_line_to_basket(request, date_id, type_id, quantity):
    """
    Adds a single ticket line to the basket

    Parameters:
    request (request object): The current request object
    date_id (String): The Ticket EventDate id in string format
    type_id (String): The Ticket TicketType id in string format
    quantity (int): The number of tickets to add to this line

    Raises:
    (TicketsNotAvailable) if not enough tickets to add item

    """
    date_total = 0
    basket = request.session.get('basket', {})

    if date_id in basket:
        # How many tickets are there already in the basket for this date?
        for type_id in basket[date_id]:
            date_total += basket[date_id][type_id]
            # Are there enough tickets available to add the new lines?
            if not check_ticket_available(date_id, date_total + quantity):
                raise TicketsNotAvailable(date_id)
        # Are we updating an existing line or adding a new one?
        if type_id in basket[date_id]:
            basket[date_id][type_id] += quantity
        else:
            basket[date_id][type_id] = quantity
    else:
        if not check_ticket_available(date_id, quantity):
            raise TicketsNotAvailable(date_id)
        basket[date_id] = {type_id: quantity}

    request.session['basket'] = basket


def update_line_in_basket(request, date_id, type_id, quantity):
    """
    Updates a single ticket line to the basket

    Parameters:
    request (request object): The current request object
    date_id (String): The Ticket EventDate id in string format
    type_id (String): The Ticket TicketType id in string format
    quantity (int): The new value for quantity

    """
    basket = request.session.get('basket', {})
    if date_id in basket:
        if type_id in basket[date_id]:
            basket[date_id][type_id] = quantity

    request.session['basket'] = basket


def remove_line_from_basket(request, date_id, type_id):
    """
    Removes a single ticket line from the basket

    Parameters:
    request (request object): The current request object
    date_id (String): The Ticket EventDate id in string format
    type_id (String): The Ticket TicketType id in string format
    """
    basket = request.session.get('basket', {})
    if date_id in basket:
        if type_id in basket[date_id]:
            del basket[date_id][type_id]
            if not basket[date_id]:
                basket.pop(date_id)

    request.session['basket'] = basket


def remove_date_from_basket(request, date_id):
    """
    Removes all tickets for a certain date

    Parameters:
    request (request object): The current request object
    date_id (String): The Ticket EventDate id in string format
    """
    basket = request.session.get('basket', {})
    if date_id in basket:
        basket.pop(date_id)

    request.session['basket'] = basket


def empty_basket(request):
    """
    Removes all tickets from the basket

    Parameters:
    request (request object): The current request object
    """
    request.session['basket'] = {}
