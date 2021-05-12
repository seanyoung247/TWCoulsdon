from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def profile(request):
    return HttpResponse(f'<h1>{request.user.username}</h1>')