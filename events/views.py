""" Defines views for the Event app """
from datetime import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import Min, Max
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Event, ShowType, EventDate, Image, Venue



def query_events(request):
    """ Gets event records based on request criteria """
    events = Event.objects.all()
    showcase_events = None
    event_type = None
    search_query = {
        'text': None,
        'fdate': None,
        'ldate': None,
        'type': None,
    }
    now = timezone.now()
    zero_date = timezone.make_aware(datetime(1, 1, 1, 0, 0))
    # Search on event type
    if 'type' in request.GET and request.GET['type']:
        event_type = request.GET['type']

        # Get all events matching criteria.
        events = (
            events.annotate(
                first_date=Min('eventdate__date'),
                # Last date is used to define if an event is still current
                # or upcoming, but some event types have no dates. If there
                # are no dates last date is set to a zero date to ensure it's
                # dealt with as if it is in the past.
                last_date=Coalesce(Max('eventdate__date'), zero_date),
            ).filter(
                    type__name=event_type,
            ).order_by('-last_date', '-first_date', '-post_date')
        )
        event_type = ShowType.objects.get(name=event_type)
        search_query['type'] = event_type
        # If showing stage shows or meetups showcase them on event dates
        if event_type in ('show', 'meet'):
            # Filter current events
            showcase_events = events.filter(last_date__gte=now)
            # Filter past events
            events = events.exclude(last_date__gte=now)
            # Otherwise showcase the latest upload
        else:
            # Returns a query set of just the first record in events
            # events is sorted by post_date so the first record is the
            # latest upload
            showcase_events = events[:1]
            # Remove the showcased event from the events list
            events = events.exclude(id=showcase_events.get().id)

    # Search for dates greater than
    if 'fdate' in request.GET and request.GET['fdate']:
        search_query['fdate'] = request.GET['fdate']
        query = timezone.make_aware(datetime.strptime(request.GET['fdate'], '%Y-%m-%d'))
        # Get events with dates later than fdate
        events = events.annotate(has_date=Max(models.Case(
            models.When(eventdate__date__gte=query, then=True),
            output_field=models.BooleanField(),
        ))).filter(has_date=True)

    # Search for dates less than
    if 'ldate' in request.GET and request.GET['ldate']:
        search_query['ldate'] = request.GET['ldate']
        query = timezone.make_aware(datetime.strptime(request.GET['ldate'], '%Y-%m-%d'))
        # Get events with dates earlier than ldate
        events = events.annotate(has_date=Max(models.Case(
            models.When(eventdate__date__lt=query, then=True),
            output_field=models.BooleanField(),
        ))).filter(has_date=True)

    # Text search
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        search_query['text'] = query
        queries = Q(title__icontains=query) | Q(description__icontains=query)
        events = events.filter(queries)

    events.order_by('-post_date')

    return {
        'showcase_events': showcase_events,
        'events': events,
        'has_next': False,
        'event_type': event_type,
        'search_query': search_query,
    }


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
        events = query_events(request)
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
        HttpResponseBadRequest('<h1>Missing page variable</h1>')

    page = int(request.GET['page'])

    events = query_events(request)['events']
    paginator = Paginator(events, settings.RESULTS_PER_PAGE)

    # If page is valid return results
    if page > 0 and page <= paginator.num_pages:
        events = paginator.page(page)
    else:
        # Silent failure
        events = None;

    # Build HTML string
    events_html = loader.render_to_string(
        'includes/events_block',
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

    context = {
        "event": event,
        "first_date": dates['min_date'],
        "last_date": dates['max_date'],
        "images": images,
    }
    return render(request, 'events/event_details.html', context)


# Venue page view
def venue_details(request, venue_id):
    """ A view to show a single venue page """
    venue = get_object_or_404(Venue, id=venue_id)

    context = {
        'venue': venue,
    }

    return render(request, 'events/venue_details.html', context)
