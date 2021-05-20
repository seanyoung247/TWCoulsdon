import json

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse

from .basket import add_line_to_basket
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


@require_POST
def add_to_basket(request):
    # Get the posted ticket list
    basket_tickets = request.POST.get('tickets')
    if basket_tickets:
        # Convert the json into an object array
        basket_tickets = json.loads(basket_tickets)

        # Iterate through the list and add to basket
        for line in basket_tickets:
            # Get the objects
            date = EventDate.objects.get(id=line['date_id'])
            ticket_type = TicketType.objects.get(id=line['type_id'])
            quantity = int(line['quantity'])

            # if the objects exist and quantity makes sense add to basket.
            # No checking for availablility is done here. Because there's no
            # 'reservation' system ticket availablility is checked at checkout
            if date and ticket_type and quantity > 0:
                add_line_to_basket(request, date.id, ticket_type.id, quantity)


    response = {
        'success': True,
    }

    return JsonResponse(response)


@require_POST
def update_basket(request):
    """ Updates a single ticket line in the basket """
    pass


@require_POST
def remove_from_basket(request):
    """ Removes a single ticket line from the basket """
    success = False

    # Get the date and type ids of the ticket line to remove
    if 'date_id' in request.POST and 'type_id' in request.POST:
        date_id = request.POST['date_id']
        type_id = request.POST['type_id']

        remove_line_from_basket(request, date_id, type_id)
        success = True


    response = {
        'success': success,
    }

    return JsonResponse(response)


#
# Reports views
#
def validate_ticket(request, ticket_id):
    """
    Gets information on a single ticket and displays
    it so it can be verified.
    """
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