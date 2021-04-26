from django.shortcuts import render
from django.db import models
from django.db.models import Min, Max
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import Coalesce
from .models import Event, ShowType, EventDate


# Event list page view 
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """

    events = Event.objects.all()
    current_events = None
    past_events = None
    event_type = None
    now = timezone.now()
    zero_date=datetime(1, 1, 1, 0, 0)
    
    if not events:
        print("null")
    
    if request.GET:
        if 'type' in request.GET:
            event_type = request.GET['type']

            # Get all events matching criteria.
            events = (
                events.annotate(
                    first_date=Min('eventdate__date'),
                    # Last date is used to define if an event is still current 
                    # or upcoming, but some event types have no dates. If there
                    # are no dates last date is set to a zero date to ensure it's
                    # dealt with as if it is in the past.
                    last_date=Coalesce(Max('eventdate__date'),zero_date),
                ).filter(
                    type__name=event_type,
                ).order_by('-last_date', '-first_date', '-post_date')
            )
            # Filter current events
            current_events = events.filter(last_date__gte=now)
            # Filter past events
            past_events = events.exclude(last_date__gte=now)

            event_type = ShowType.objects.get(name=event_type)

    context = {
        'event_type': event_type,
        'current_events': current_events,
        'past_events': past_events,
        'events': events,
    }
    
    return render(request, 'events/events.html', context )
    

# Event page view

# Venue page view 