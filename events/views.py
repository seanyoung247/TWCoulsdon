from django.shortcuts import render
from .models import Event, ShowType

# Event list page view 
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """

    types = None
    events = None
    
    if request.GET:
        if 'type' in request.GET:
            types = request.GET['type'].split(',')
            events = Event.objects.filter(type__name__in=types)
    
    
    context = {
        'events': events,
    }
    
    return render(request, 'events/events.html', context )
    

# Event page view

# Venue page view 