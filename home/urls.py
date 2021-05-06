from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<category_slug>/', views.category, name='category'),
    path('<page_slug>/', views.page, name='page'),
]
