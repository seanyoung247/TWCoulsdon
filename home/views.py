""" Provides the views for the home and infomation pages """
from django.http import Http404
from django.shortcuts import render, reverse, get_object_or_404
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
                models.When(eventdate__date__gte=now, then=1),
                models.When(eventdate__date__lt=now, then=0),
                output_field=models.IntegerField(),
            )),
            # Get the first event date for sorting
            first_date=Min('eventdate__date'),
            last_date=Max('eventdate__date'),
        ).filter(current=True).order_by('-first_date', '-post_date')[:4]
    )
    # Add the events to home_items
    for event in events:
        home_items.append({
            'image': event.title_image.image,
            'title': event.title,
            'text': event.tagline,
            'first_date': event.first_date,
            'last_date': event.last_date,
            'link': reverse('event_details', args=(event.slug,)),
        })

    # Get standard items: about us, join us etc
    categories = Category.objects.all()[:4]
    for category in categories:
        # Only show a category if it has a title_page
        if category.title_page:
            home_items.append({
                'image': category.title_page.image,
                'title': category.title_page.title,
                'text': category.title_page.description,
                'first_date': None,
                'last_date': None,
                'link': reverse('category_page', args=(category.slug,)),
            })

    context = {
        'home_items': home_items,
    }

    return render(request, 'home/index.html', context)


def category_page(request, category_slug):
    """ A view to show single category pages """
    # Get the category
    category = get_object_or_404(Category, slug=category_slug)
    page = None
    # Are we getting a page variable?
    if 'page' in request.GET:
        # Get the page referenced in the parameter
        page = get_object_or_404(Page, slug=request.GET['page'])
    else:
        # Else get the category title page_links
        page = category.title_page

    # If there's no page, we can't load it...
    if not page:
        raise Http404

    # Get this category's page links - Note: If this section becomes more than
    # static information to some sort of blog format we'll need to do pagination here.
    page_links = Page.objects.filter(category=category.id)
    context = {
        'category': category,
        'page': page,
        'page_links': page_links,
    }

    return render(request, 'home/page.html', context)
