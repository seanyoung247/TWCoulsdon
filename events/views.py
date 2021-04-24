from django.shortcuts import render

# Event list page view 
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """
    return render(request, 'events/events.html')
    

# Event page view

# Venue page view 