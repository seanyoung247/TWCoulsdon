from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_events, name='list_events')
]
