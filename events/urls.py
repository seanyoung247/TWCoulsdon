""" Defines url paths used by the Event App """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='events'),
    path('lazy_load/', views.lazy_load_events, name='lazy_load_events'),
    path('venue/<venue_id>', views.venue_details, name='venue_details'),
    path('edit_event/', views.edit_event, name='edit_event'),
    path('edit_event/delete_event/', views.delete_event, name='delete_event'),
    path('edit_event/remove_date/', views.remove_date, name='remove_date'),
    path('edit_event/add_image/', views.add_image, name='add_image'),
    path('edit_event/edit_image/', views.edit_image, name='edit_image'),
    path('edit_event/remove_image/', views.remove_image, name='remove_image'),
    path('edit_event/set_title_image/', views.set_title_image, name='set_title_image'),
    path('<event_slug>/', views.event_details, name='event_details'),
]
