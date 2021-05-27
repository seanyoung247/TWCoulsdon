""" Defines views for the Event app """
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.db.models import Min, Max
from django.template import loader
from django.core.paginator import Paginator
from django.http import JsonResponse

from boxoffice.models import TicketType
from .queries import query_events
from .models import Event, ShowType, EventDate, Image, Venue
from .forms import EventDateForm, ImageForm, EventForm


# Event list page view
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """
    events = {
        'showcase_events': None,
        'events': None,
        'has_next': False,
        'event_type': None,
        'search_query': {
            'text': None,
            'fdate': None,
            'ldate': None,
            'type': None,
        }
    }
    event_types = None

    if request.GET:
        events = query_events(request.GET)
        # Are there more events than can be shown in a single page?
        events['has_next'] = events['events'].count() > settings.RESULTS_PER_PAGE
        # Ensure there's only a single page of results
        events['events'] = events['events'][:settings.RESULTS_PER_PAGE]

    # Get all event types (for filling out search dropdown)
    event_types = ShowType.objects.all()
    context = {
        'search_query': events['search_query'],
        'event_type': events['event_type'],
        'event_types': event_types,
        'showcase_events': events['showcase_events'],
        'events': events['events'],
        'has_next': events['has_next'],
    }

    return render(request, 'events/events.html', context)


def lazy_load_events(request):
    """ Returns the next page of results based on search criteria """

    if 'page' not in request.GET or not request.GET['page']:
        messages.error(request, "Can't get results, no page specified.")

    page = int(request.GET['page'])

    events = query_events(request.GET)['events']
    paginator = Paginator(events, settings.RESULTS_PER_PAGE)

    # If page is valid return results
    if 0 < page >= paginator.num_pages:
        events = paginator.page(page)
    else:
        # Silent failure
        events = None

    # Build HTML string
    events_html = loader.render_to_string(
        'includes/events_block.html',
        {'events': events}
    )
    # Build JSON response
    response = {
        'pages': events_html,
        'more_pages': events.has_next(),
    }
    return JsonResponse(response)


# Event page view
def event_details(request, event_slug):
    """ A view to show a single event page """
    # Get the event
    event = get_object_or_404(Event, slug=event_slug)
    # Gets the first and last dates associated with this event
    dates = EventDate.objects.filter(event=event).aggregate(
        min_date=Min('date'), max_date=Max('date')
    )
    # Get this event's gallery images
    images = Image.objects.filter(event=event)

    # Get the ticket types
    ticket_types = TicketType.objects.all()

    context = {
        "event": event,
        "ticket_types": ticket_types,
        "first_date": dates['min_date'],
        "last_date": dates['max_date'],
        "images": images,
    }
    return render(request, 'events/event_details.html', context)


def edit_event(request):
    """ A view to show the event add/edit form """
    event = None
    dates = None
    images = None

    if request.method == 'POST':
        try:
            # Get the event data
            event_data = {
                'title': request.POST['title'],
                'author': request.POST['author'],
                'tagline': request.POST['tagline'],
                'description': request.POST['description'],
                'type': request.POST['type'],
                'venue': request.POST['venue'],
                'content': request.POST['content'],
            }
    else:
        # Is there an event variable in the request?
        if 'event' in request.GET:
            # Get the event
            event = get_object_or_404(Event, id=int(request.GET['event']))
            # Get associated objects
            dates = EventDate.objects.filter(event=event)
            images = Image.objects.filter(event=event)

            event_form = EventForm(instance=event)
            image_form = ImageForm()
        else:
            event_form = EventForm()
            image_form = ImageForm()

    context = {
        'event': event,
        'dates': dates,
        'images': images,
        'event_form': event_form,
    }
    return render(request, 'events/edit_event.html', context)


# Venue page view
def venue_details(request, venue_id):
    """ A view to show a single venue page """
    venue = get_object_or_404(Venue, id=venue_id)

    context = {
        'venue': venue,
    }

    return render(request, 'events/venue_details.html', context)
