""" Tools for creating, updating and deleting tickets """
from events.models import Event, EventDate
from .models import TicketType, Ticket, Order
from .queries import get_available_tickets_for_date


def check_ticket_available(event_date, quantity):
    """ Checks that there are enough tickets left for the date passed

    Parameters:
    date (EventDate): Date to check
    quantity (int): Quantity required

    Returns:
    (boolean): True if enough tickets left
    """
    return (get_available_tickets_for_date(event_date) >= quantity)


def check_tickets_available():
    """
    Parameters:

    Returns:

    """
    pass