from django.shortcuts import render
from django.http import HttpResponse


def boxoffice(request):
    return HttpResponse('<h1>boxoffice</h1>')