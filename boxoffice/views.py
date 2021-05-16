from django.shortcuts import render
from django.http import HttpResponse
from .reports import generate_ticket_pdf


def boxoffice(request):
    return generate_ticket_pdf()