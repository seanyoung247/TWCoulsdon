""" Template tags for the event app """

from django import template
from django.utils import timezone

from boxoffice.queries import get_available_tickets_for_event

register = template.Library()


@register.filter(name='has_tickets')
def has_tickets(event):
    """ Returns true if event still has tickets """
    return (get_available_tickets_for_event(event) > 0)


@register.filter(name='ticket_count')
def ticket_count(event):
    """ Returns the number of tickets still available for an event """
    return get_available_tickets_for_event(event)