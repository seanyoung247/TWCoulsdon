""" Defines views for the Event app """
import json

from datetime import datetime
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.db.models import Min, Max
from django.template import loader
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone

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


@staff_member_required
def edit_event(request):
    """ A view to show the event add/edit form """
    event = None
    dates = None
    images = None
    success = False
    event_url = None
    message_html = ""

    if request.method == 'POST':
        try:
            # Is this an existing event?
            if 'event_id' in request.POST:
                event = Event.objects.get(id=request.POST['event_id'])
            # Create the event data
            event_data = {
                'title': request.POST['title'],
                'author': request.POST['author'],
                'tagline': request.POST['tagline'],
                'description': request.POST['description'],
                'type': request.POST['type'],
                'venue': request.POST['venue'],
                'content': request.POST['content'],
            }

            if event:
                event_form = EventForm(event_data, instance=event)
            else:
                event_form = EventForm(event_data)
            # Is the data valid?
            if event_form.is_valid():
                event = event_form.save()

            # Create the event dates
            for date in json.loads(request.POST['dates']):
                date_data = {
                    'event': event,
                    'date': f"{date['date']} {date['time']}",
                }
                if int(date['date_id']) > 0:
                    date_form = EventDateForm(date_data,
                        instance=EventDate.objects.get(id=date['date_id']))
                else:
                    date_form = EventDateForm(date_data)

                if date_form.is_valid():
                    date_form.save()

            success = True

        except KeyError:
            messages.error(request, "Unable to update event: missing required data. \
                Please check your submission and try again.")
            success = False

        except Event.DoesNotExist:
            messages.error(request, "Unable to update event: event not found.")
            success = False

        except EventDate.DoesNotExist:
            messages.error(request, "Unable to update event: dates not found.")
            success = False

        # Create the event url
        event_url = reverse('event_details', args=[event.slug])
        # If there was a failure, render any messages
        if not success:
            message_html = loader.render_to_string('includes/messages.html', request=request)
        response = {
            'success': success,
            'event_url': event_url,
            'message_html': message_html,
        }
        return JsonResponse(response)

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


@staff_member_required
@require_POST
def remove_date(request):
    success = False;
    if 'date_id' in request.POST:
        try:
            # Get the event to delete
            event_date = EventDate.objects.get(id=request.POST['date_id'])
            event_date.delete()
        except EventDate.DoesNotExist:
            message.error(request, "Can't remove date: Does not exist.")
    else:
        message.error(request, "Can't remove date: No date id provided.")

    message_html = loader.render_to_string('includes/messages.html', request=request)
    response = {
        'success': True,
        'message_html': message_html,
    }
    return JsonResponse(response)


@staff_member_required
@require_POST
def add_image(request):
    return JsonResponse({'success':True})


@staff_member_required
@require_POST
def edit_image(request):
    return JsonResponse({'success':True})


@staff_member_required
@require_POST
def remove_image(request):
    return JsonResponse({'success':True})


# Venue page view
def venue_details(request, venue_id):
    """ A view to show a single venue page """
    venue = get_object_or_404(Venue, id=venue_id)

    context = {
        'venue': venue,
    }

    return render(request, 'events/venue_details.html', context)
