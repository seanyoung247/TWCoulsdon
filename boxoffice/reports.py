""" Generates pdf reports and tickets """
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template.loader import render_to_string
#from django.utils.text import slugify
from django.conf import settings

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from .models import TicketType, Ticket, Order


def generate_ticket_pdf(request, order):
    """ Generates a pdf of the tickets in a given order

    Parameters:
    request (Request): The request object
    order (Order): The order to generate tickets for

    Returns:
    A byte buffer of the generated pdf
    """

    # Get tickets for this order
    tickets = Ticket.objects.filter(order=order)

    # Generate a html template for the ticket
    context = {
        'order': order,
        'tickets': tickets,
        'request': request,
    }
    html = render_to_string('tickets/ticket.html', context)

    # Generate a pdf from the HTML
    font_config = FontConfiguration()
    return HTML(string=html, base_url=request.build_absolute_uri()
                ).write_pdf(font_config=font_config)



