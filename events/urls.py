""" Defines url paths used by the Event App """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='events'),
    path('venue/<venue_id>', views.venue_details, name='venue_details'),
    path('<event_slug>', views.event_details, name='event_details'),
]
