from django.shortcuts import render
from django.http import HttpResponse
from .reports import generate_ticket_pdf
from .models import Order


def boxoffice(request):
    order = Order.objects.get(pk=1)
    return generate_ticket_pdf(request, order)


def validate_ticket(request, ticket_id):
    return HttpResponse("<h1>Test Ticket</h1>")
