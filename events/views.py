from django.shortcuts import render
from django.db import models
from django.db.models import Min, Max
from datetime import datetime
from django.utils import timezone
from .models import Event, ShowType, EventDate

# Event list page view 
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """

    events = Event.objects.all()
    event_types = None
    now = timezone.now()
    
    if not events:
        print("null")
    
    if request.GET:
        if 'type' in request.GET:
            # Only filter on dates for productions
            event_types = request.GET['type'].split(',')
            events = (
                events.annotate(
                    # Is this event in the future or past?
                    current=models.Case(
                        models.When(eventdate__date__gte=now, then=True),
                        models.When(eventdate__date__lt=now, then=False),
                        output_field=models.BooleanField(),
                    ),
                    # Get the first event date for sorting
                    first_date=Min('eventdate__date')
                ).filter(
                    # Filter on required show type
                    type__name__in=event_types
                # Order by inital date and id in decending order (latest to earliest)
                # Ensuring current events are grouped first
                ).order_by('-current', '-first_date', '-id')
            )
            event_types = ShowType.objects.filter(name__in=event_types)

    past_events=events.filter(current=False)
    showcase_events=events.filter(current=True)
    context = {
        'event_types': event_types,
        'events': events,
        'past_events': past_events,
        'showcase_events': showcase_events,
    }
    
    return render(request, 'events/events.html', context )
    

# Event page view

# Venue page view 