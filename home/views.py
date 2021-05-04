from django.shortcuts import render, reverse
from django.db import models
from django.db.models import Min, Max
from django.utils import timezone
from events.models import Event
from .models import Category, Page


def index(request):
    """ A view for showing the landing page """
    home_items = []
    now = timezone.now()
    # Get any events with dates in the future (maximum of 4)
    events = list(Event.objects.filter(type__name__in={'show','meet'}
        ).annotate(
            # Has this event got at least one date in the future
            current=Max(models.Case(
                models.When(eventdate__date__gte=now, then=True),
                models.When(eventdate__date__lt=now, then=False),
                output_field=models.BooleanField(),
            )),
            # Get the first event date for sorting
            first_date=Min('eventdate__date'),
            last_date=Max('eventdate__date'),
        ).filter(current=True).order_by('-first_date', '-post_date')[:4]
    )
    # Add the events to home_items
    for event in events:
        home_items.append({
            'image': event.title_image.image.url,
            'title': event.title,
            'text': event.tagline,
            'first_date': event.first_date,
            'last_date': event.last_date,
            'link': reverse('event_details', args=(event.slug,)),
        })

    # Get standard items: about us, join us
    categories = Category.objects.all()[:4]
    for category in categories:
        if category.title_page:
            home_items.append({
                'image': category.title_page.image.url,
                'title': category.title_page.title,
                'text': category.title_page.description,
                'first_date': None,
                'last_date': None,
                'link': category.slug,
            })

    context = {
        "home_items": home_items,
    }

    return render(request, 'home/index.html', context)