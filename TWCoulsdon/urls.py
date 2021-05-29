"""TWCoulsdon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views
from boxoffice import views as boxoffice_views

urlpatterns = [
    path('favicon.ico', core_views.redirect_ico),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),

    path('', include('home.urls')),
    path('events/', include('events.urls')),
    path('profile/', include('profiles.urls')),
    path('boxoffice/', include('boxoffice.urls')),
    path('ticket/<ticket_id>', boxoffice_views.validate_ticket, name='validate_ticket')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found_view'
# Allows testing of custom error pages
if settings.DEBUG:
    urlpatterns.append(path('404/', core_views.page_not_found_view))
