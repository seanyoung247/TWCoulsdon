from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('twc/<category_slug>/', views.category, name='category'),
    path('twc/<page_slug>/', views.page, name='page'),
]
