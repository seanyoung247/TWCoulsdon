from django.urls import path
from . import views

urlpatterns = [
    path('', views.boxoffice, name='boxoffice'),
]
