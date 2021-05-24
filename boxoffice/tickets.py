""" Tools for creating, updating and deleting tickets """
import json

from events.models import EventDate
from .models import TicketType, Ticket
from .queries import get_available_tickets_for_date


def check_ticket_available(event_date, quantity):
    """
    Checks that there are enough tickets left for the date passed

    Parameters:
    date (EventDate): Date to check
    quantity (int): Quantity required

    Returns:
    (boolean): True if enough tickets left

    """
    return get_available_tickets_for_date(event_date) >= quantity


def collapse_ticket_lines(basket):
    """
    Collapses ticket lines into a single quantity for each date

    Parameters:
    basket (Basket Dictionary): The basket to collapse

    Returns:
    (Dictionary): The collapsed dictionary

    """
    ticket_dates = {}
    for date_id in basket:
        for type_id in basket[date_id]:
            if date_id in ticket_dates:
                ticket_dates[date_id] += basket[date_id][type_id]
            else:
                ticket_dates[date_id] = basket[date_id][type_id]
    return ticket_dates;


def check_basket_availability(basket):
    """
    Checks all ticket lines in a basket are available

    Parameters:
    basket (Basket Dictionary): The basket to check

    Raises:
    (TicketsNotAvailable): If a ticket line can't be fulfilled

    """
    # Collapse different ticket types in the basket to a single
    # quantity for each date
    ticket_dates = collapse_ticket_lines(basket)

    # Check the availability for each date.
    for date in ticket_dates:
        #Get the event date for this id
        event_date = EventDate.objects.get(id=date)
        if not check_ticket_available(event_date, ticket_dates[date]):
            # If a given date has too few ticket, raise an exception
            raise TicketsNotAvailable(date)


def check_order_availabillity(order):
    """
    Checks all ticket lines in an order are available

    Parameters:
    order (Order): The order details to check

    Raises:
    (TicketsNotAvailable): If a ticket line can't be fulfilled

    """
    # Get the basket from the order
    basket = json.loads(order.original_basket)

    check_basket_availability(basket)


def create_tickets_for_order(order):
    """
    Creates tickets for a given order.

    Parameters:
    order (Order): The order to create tickets for

    Raises:
    EmptyOrder: If basket is empty
    TicketsNotAvailable: If tickets are not available

    """

    # Get the basket from the order
    if not order.original_basket:
        raise EmptyOrder

    basket = json.loads(order.original_basket)

    # Ensure there's actual tickets to create
    if not basket:
        raise EmptyOrder

    # Check that there are enough available tickets
    check_basket_availability(basket)

    # Step through the ticket lines creating the required tickets
    for date_id in basket:
        # Get the current event date object
        event_date = EventDate.objects.get(id=date_id)
        for type_id in basket[date_id]:
            # Get the current ticket type
            ticket_type = TicketType.objects.get(id=type_id)
            # Construct the number of tickets required
            for _ in range(basket[date_id][type_id]):
                Ticket.objects.create(
                    order=order,
                    type=ticket_type,
                    event=event_date.event,
                    date=event_date,
                )


class EmptyOrder(Exception):
    """ Raised when creating tickets from an order with an empty basket """
    def __init__(self):
        # Create the exception
        Exception.__init__(self, "No tickets in order")


class TicketsNotAvailable(Exception):
    """ Raised if a ticket line can not be fulfilled """
    def __init__(self, date_id):
        # Create the exception
        Exception.__init__(self, "Not enough tickets to fulfill order")
        # Set properties
        self.date_id = date_id
