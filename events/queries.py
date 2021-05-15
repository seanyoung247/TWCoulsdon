""" Defines general use queries for event app objects """
from datetime import datetime

from django.db import models
from django.db.models import Q
from django.db.models import Min, Max
from django.utils import timezone
from django.db.models.functions import Coalesce

#from core.debug import debug_print

from .models import Event, ShowType


#TODO: Split query events into sub functions


def query_events(query_list):
    """ Gets event records based on request criteria

    Parameters:
    query_list (list of strings): The list of query Parameters

    Returns:
    search query (dictionary): Returns a dictionary describing the
                               query and results in the following format:
        return = {
            showcase_events: <query_set of showcase events> or None
            events: <query_set of non-showcase events> or None
            has_next: For reciever pagination use. Always false
            event_type: <ShowType object> or None
            search_query = {
                text: <the text string query passed> or None
                fdate: <the first date in ISO8601 format> or None
                ldate: <the last date in ISO8601 format> or None
                type: <the string event type> or None
            }
        }
    """

    events = Event.objects.all().order_by('-post_date')
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

    # Search for dates greater than
    if 'fdate' in query_list and query_list['fdate']:
        search_query['fdate'] = query_list['fdate']
        query = timezone.make_aware(datetime.strptime(query_list['fdate'], '%Y-%m-%d'))
        # Get events with dates later than fdate
        events = events.annotate(has_date=Max(models.Case(
            models.When(eventdate__date__gte=query, then=1),
            output_field=models.IntegerField(),
        ))).filter(has_date=True)

    # Search for dates less than
    if 'ldate' in query_list and query_list['ldate']:
        search_query['ldate'] = query_list['ldate']
        query = timezone.make_aware(datetime.strptime(query_list['ldate'], '%Y-%m-%d'))
        # Get events with dates earlier than ldate
        events = events.annotate(has_date=Max(models.Case(
            models.When(eventdate__date__lt=query, then=1),
            output_field=models.IntegerField(),
        ))).filter(has_date=True)

    # Text search
    if 'q' in query_list and query_list['q']:
        query = query_list['q']
        search_query['text'] = query
        queries = Q(title__icontains=query) | Q(description__icontains=query)
        events = events.filter(queries)

    # Search on event type
    if 'type' in query_list and query_list['type']:
        event_type = query_list['type']

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
        if str(event_type) in ('show', 'meet'):
            # Filter current events
            showcase_events = events.filter(last_date__gte=now)
            # Filter past events
            events = events.exclude(last_date__gte=now)
        # Otherwise showcase the latest upload
        else :
            # Returns a query set of just the first record in events
            # events is sorted by post_date so the first record is the
            # latest upload
            showcase_events = events[:1]
            if showcase_events:
                # Remove the showcased event from the events list
                events = events.exclude(id=showcase_events.get().id)

    return {
        'showcase_events': showcase_events,
        'events': events,
        'has_next': False,
        'event_type': event_type,
        'search_query': search_query,
    }
