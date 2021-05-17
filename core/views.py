from django.shortcuts import render, redirect
from django.conf import settings


def redirect_ico(request):
    """ Redirects any errant requests for the favicon to it's true location """
    return redirect(settings.FAVICON)