""" Generates reports and tickets in pdf and csv formats """
from __future__ import unicode_literals

import json
#from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from events.models import Event, EventDate
from .models import TicketType, Ticket, Order
from .basket import get_ticket_lines_from_basket


def report_tickets_for_event(request, event):
    """
    Generates a pdf of the tickets in a given order

    Parameters:
    request (Request): The request object
    order (Order): The event to generate a report for

    Returns:
    TBD
    """
    pass


def report_tickets_for_date(request, date):
    """
    Generates a pdf of the tickets in a given order

    Parameters:
    request (Request): The request object
    date (EventDate): The date to generate a report for

    Returns:
    TBD
    """
    pass


def generate_ticket_pdf(request, order):
    """
    Generates a pdf of the tickets in a given order

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
    ticket_pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(font_config=font_config)

    return ticket_pdf


def send_ticket_pdf_email(request, order):
    """
    Sends a pdf for the tickets in a given order via email on the order.

    Parameters:
    request (Request): The request object
    order (Order): The order to send tickets for
    """
    ticket_pdf = generate_ticket_pdf(request, order)
    order_basket = get_ticket_lines_from_basket(json.loads(order.original_basket))

    context={
        'order': order,
        'items': order_basket,
    }

    subject = render_to_string('email/order_subject.txt', context)
    content = render_to_string('email/order_html_content.html', context)

    msg = EmailMessage(
        subject,
        content,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )
    msg.content_subtype = 'html'
    msg.attach('tickets.pdf', ticket_pdf, 'application/pdf')
    msg.send()


def send_ticket_pdf_http(request, order):
    """
    Constructs a HTTP response and embeds a pdf of the tickets
    in a given order.

    Parameters:
    request (Request): The request object
    order (Order): The order to send tickets for

    Returns:
    (HttpResponse)
    """
    ticket_pdf = generate_ticket_pdf(request, order)

    response = HttpResponse(ticket_pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; tickets.pdf'

    return response
