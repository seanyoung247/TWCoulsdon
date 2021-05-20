from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse

from .reports import generate_ticket_pdf
from .models import TicketType, Ticket, Order

from events.models import Event, EventDate
from events.queries import get_remaining_event_dates


# Not currently used, will probably remove -
def boxoffice(request):
    pass

#
# Add tickets dialog views
#
def buy_tickets(request):
    """ Provides the event form data and passes it to the frontend as json """

    if 'event' not in request.GET or not request.GET['event']:
        HttpResponseBadRequest('<h1>Missing event variable</h1>')

    event = get_object_or_404(Event, id=request.GET['event'])
    dates = get_remaining_event_dates(event).order_by('date')
    ticket_types = TicketType.objects.all()

    context = {
        'dates': dates,
        'ticket_types': ticket_types,
    }
    form_html = loader.render_to_string(
        'includes/add_ticket_form.html', context)

    response = {
        'form': form_html,
    }

    return JsonResponse(response)


#
# Shopping Basket views
#
def view_basket(request):
    return render(request, 'boxoffice/basket.html');


def add_to_basket(request):
    pass


def remove_from_basket(request):
    pass


#
# Reports views
#
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