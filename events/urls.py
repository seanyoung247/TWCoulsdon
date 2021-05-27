""" Defines url paths used by the Event App """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='events'),
    path('lazy_load/', views.lazy_load_events, name='lazy_load_events'),
    path('venue/<venue_id>', views.venue_details, name='venue_details'),
    path('edit_event/', views.edit_event, name='edit_event'),
    path('edit_event/remove_date/', views.remove_date, name='remove_date'),
    path('<event_slug>/', views.event_details, name='event_details'),
]
