from django.shortcuts import render
from django.db import models
from django.db.models import Min, Max
from datetime import datetime
from .models import Event, ShowType, EventDate

# Event list page view 
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """

    types = None
    events = None
    now = datetime.now()
    
    if request.GET:
        if 'type' in request.GET:
            types = request.GET['type'].split(',')
            events = (
                Event.objects.annotate(
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
                    type__name__in=types
                # Order by inital date in decending order (latest to earliest)
                ).order_by('-first_date')
            )

    
    context = {
        'events': events,
    }
    
    return render(request, 'events/events.html', context )
    

# Event page view

# Venue page view 