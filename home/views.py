from django.shortcuts import render


def index(request):
    """ A view to return the index page """
    #TODO: Get carousel data here
    return render(request, 'home/index.html')