from django.urls import path
from . import views

urlpatterns = [
    #path('', views.boxoffice, name='boxoffice'),
    path('buy_tickets/', views.buy_tickets, name="buy_tickets"),
    path('basket/', views.view_basket, name="view_basket"),
    path('basket/add/', views.add_to_basket, name="add_to_basket"),
    path('basket/remove/', views.remove_from_basket, name='remove_from_basket'),
]
