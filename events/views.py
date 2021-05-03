""" Defines views for the Event app """
from datetime import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.db.models import Min, Max

from django.utils import timezone
from django.db.models.functions import Coalesce
from .models import Event, ShowType, EventDate, Image, Venue


# Event list page view
def list_events(request):
    """ A view to show all events, and allows sorting and searching of queries """

    events = Event.objects.all()
    showcase_events = None
    event_type = None
    now = timezone.now()
    zero_date = timezone.make_aware(datetime(1, 1, 1, 0, 0))

    search_query = {
        'text': None,
        'fdate': None,
        'ldate': None,
        'type': None,
    }

    if request.GET:
        # Search on event type
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
                # events is sorted by post_date so the first record is the
                # latest upload
                showcase_events = events[:1]
                # Remove the showcased event from the events list
                events = events.exclude(id=showcase_events.get().id)

        # Search for dates greater than
        if 'fdate' in request.GET:
            search_query['fdate'] = request.GET['fdate']
            query = timezone.make_aware(datetime.strptime(request.GET['fdate'], '%Y-%m-%d'))
            # Get events with dates later than fdate
            events = events.annotate(has_date=Max(models.Case(
                models.When(eventdate__date__gte=query, then=True),
                output_field=models.BooleanField(),
            ))).filter(has_date=True)

        # Search for dates less than
        if 'ldate' in request.GET:
            search_query['ldate'] = request.GET['ldate']
            query = timezone.make_aware(datetime.strptime(request.GET['ldate'], '%Y-%m-%d'))
            # Get events with dates earlier than ldate
            events = events.annotate(has_date=Max(models.Case(
                models.When(eventdate__date__lt=query, then=True),
                output_field=models.BooleanField(),
            ))).filter(has_date=True)

        # Text search
        if 'q' in request.GET:
            query = request.GET['q']
            search_query['text'] = query
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('events'))

            queries = Q(title__icontains=query) | Q(description__icontains=query)
            events = events.filter(queries)


    context = {
        'search_query': search_query,
        'event_type': event_type,
        'showcase_events': showcase_events,
        'events': events,
    }

    return render(request, 'events/events.html', context)


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
