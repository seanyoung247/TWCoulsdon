""" Defines the boxoffice app's routes """
from django.urls import path
from . import views

urlpatterns = [
    #path('', views.boxoffice, name='boxoffice'),
    # Add Ticket Dialog
    path('buy_tickets/', views.buy_tickets, name="buy_tickets"),
    # Shopping Basket
    path('basket/', views.view_basket, name="view_basket"),
    path('basket/add/', views.add_to_basket, name="add_to_basket"),
    path('basket/remove/', views.remove_from_basket, name='remove_from_basket'),
    path('basket/update/', views.update_basket, name='update_basket'),
    # Checkout
    path('checkout/', views.checkout, name='checkout')
    # Reports
]
