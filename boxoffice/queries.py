""" Defines general queries for use throughout the site """
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from events.models import Event, EventDate, Venue
from .models import TicketType, Ticket, Order


def get_available_tickets_for_date(event_date):
    """ Returns the number of tickets available for a given event date.

    Parameters:
    event_date (EventDate): The EventDate to check

    Returns:
    int: Number of avaliable tickets

    """
    if event_date is None: return 0

    # We can't sell tickets for an event in the past.
    ticket_cutoff = timezone.now() - timedelta(hours = settings.TICKET_CUT_OFF_HOURS)
    if event_date.date < ticket_cutoff: return 0

    # How many tickets have already been sold?
    ticket_count = Ticket.objects.filter(date=event_date).count()
    # How many seats does the venue have?
    venue_seats = event_date.event.venue.capacity if event_date.event.venue is not None else 0
    return venue_seats - ticket_count

    return 0


def get_available_tickets_for_event(event):
    """ Returns the number of tickets available for a given event.

    Parameters:
    event (Event): The Event to check

    Returns:
    int: Number of avaliable tickets

    """
    if event is None: return 0

    ticket_cutoff = timezone.now() - timedelta(hours = settings.TICKET_CUT_OFF_HOURS)

    # How many tickets have been sold for future events?
    ticket_count = Ticket.objects.filter(
        event=event, date__date__gte=ticket_cutoff).count()

    # How many dates are left?
    date_count = EventDate.objects.filter(event=event, date__gte=ticket_cutoff).count()
    # How many are there in total?
    venue_seats = (event.venue.capacity if event.venue is not None else 0) * date_count
    return venue_seats - ticket_count

    return 0





