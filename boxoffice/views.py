from django.shortcuts import render
from django.http import HttpResponse

from .reports import generate_ticket_pdf
from .models import Ticket, Order

from events.queries import get_future_events


def boxoffice(request):
    pass


def basket(request):
    pass


def validate_ticket(request, ticket_id):
    # Get ticket information
    ticket = Ticket.objects.get(ticket_id=ticket_id)

    context = {
        'ticket': ticket,
    }

    return render(request, 'tickets/validate_ticket.html', context)



# Code Snippet to create and return tickets from an order.
# TODO: DELETE THIS!!!
    # order = Order.objects.get(pk=1)
    #
    # pdf = generate_ticket_pdf(request, order)
    #
    # # Prepare the response headers
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; tickets.pdf'
    #
    # return response