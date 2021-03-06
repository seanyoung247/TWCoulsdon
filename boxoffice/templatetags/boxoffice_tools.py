""" Template tags for the event app """
from datetime import timedelta
import json

from django import template
from django.utils import timezone
from django.shortcuts import reverse

import segno

from events.models import Event, EventDate
from boxoffice.queries import get_available_tickets_for_event, get_available_tickets_for_date
from boxoffice.basket import get_ticket_lines_from_basket

register = template.Library()


@register.filter(name='ticket_count')
def ticket_count(event):
    """ Returns the number of tickets still available for an event or date """
    if isinstance(event, Event):
        return get_available_tickets_for_event(event)
    if isinstance(event, EventDate):
        return get_available_tickets_for_date(event)

    return 0


@register.filter(name='has_tickets')
def has_tickets(event):
    """ Returns true if event or date still has tickets """
    return ticket_count(event) > 0


@register.filter(name='expired')
def expired(ticket):
    """ returns whether the ticket passed has expired """
    return ticket.date.date < (timezone.now() + timedelta(hours=2))


@register.simple_tag
def validate_ticket_url(request, ticket_id):
    """ Constructs a validation url for the ticket_id passed """
    return request.build_absolute_uri(reverse('validate_ticket', args=(ticket_id,)))


@register.simple_tag
def ticket_qr_code(request, ticket_id):
    """ Generates a qr code data url to validate a ticket with the id passed """
    return segno.make(
            validate_ticket_url(request, ticket_id),
            micro=False
        ).svg_data_uri(scale=2)


@register.filter(name='format_basket')
def format_basket(basket):
    """ Formats a text basket (such as one stashed in an order) into an object list """
    return get_ticket_lines_from_basket(json.loads(basket))
