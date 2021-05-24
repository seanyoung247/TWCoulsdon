""" Defines the paths for the home app """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('twc/<category_slug>/', views.category_page, name='category_page'),
]
