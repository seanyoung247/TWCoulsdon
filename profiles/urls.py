from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history')
    #path('load_order_page/<page>', views.load_order_page, name='load_order_page'),
]
