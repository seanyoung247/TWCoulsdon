from django.shortcuts import render

# Create your views here.
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """
    return render(request, 'events/events.html')