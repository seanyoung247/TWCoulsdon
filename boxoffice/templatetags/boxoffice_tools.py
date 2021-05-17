""" Template tags for the event app """
from django import template
from django.utils import timezone

from events.models import Event, EventDate
from boxoffice.queries import get_available_tickets_for_event, get_available_tickets_for_date

register = template.Library()


@register.filter(name='ticket_count')
def ticket_count(event):
    """ Returns the number of tickets still available for an event or date """
    if isinstance(event, Event):
        return get_available_tickets_for_event(event)
    elif isinstance(event, EventDate):
        return get_available_tickets_for_date(event)
    return 0


@register.filter(name='has_tickets')
def has_tickets(event):
    """ Returns true if event or date still has tickets """
    return (ticket_count(event) > 0)
