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
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/cache_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),
    # Reports
    path('tickets/<order_number>/', views.get_tickets, name='get_tickets'),
]
