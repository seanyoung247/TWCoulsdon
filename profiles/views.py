from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def profile(request):
    return HttpResponse('<h1>profiles</h1>')