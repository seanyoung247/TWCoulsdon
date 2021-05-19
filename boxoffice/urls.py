from django.urls import path
from . import views

urlpatterns = [
    path('', views.boxoffice, name='boxoffice'),
    path('buy_tickets/', views.buy_tickets, name="buy_tickets"),
]
