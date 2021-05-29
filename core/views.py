""" Defines general views not related to specific apps """
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings


def redirect_ico(request):
    """ Redirects any errant requests for the favicon to it's true location """
    return redirect(settings.FAVICON)


def page_not_found_view(request, exception=None):
    """ A view to render custom 404 not found page """
    if exception:
        messages.error(request, f"error encountered: {exception}")

    return render(request, 'errors/404.html')
