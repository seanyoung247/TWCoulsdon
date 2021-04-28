from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='events'),
    path('<event_slug>', views.event_details, name='event_details'),
]
