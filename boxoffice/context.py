from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from events.models import Event, EventDate
from boxoffice.models import TicketType

def basket_contents(request):

    basket_items = []
    item_count = 0
    total = 0

    basket = request.session.get('basket', {})

    for date_id in basket:
        # Get the event date
        date = get_object_or_404(EventDate, id=date_id)

        for type_id in basket[date_id]:
            ticket_type = get_object_or_404(TicketType, id=type_id)
            line_total = ticket_type.price * basket[date_id][type_id]
            total += line_total

            basket_items.append({
                'event': date.event,
                'date': date,
                'ticket_type': ticket_type,
                'quantity': basket[date_id][type_id],
                'line_total': line_total,
            })

    context = {
        'basket': {
            'items': basket_items,
            'item_count': item_count,
            'total': total,
        }
    }

    return context