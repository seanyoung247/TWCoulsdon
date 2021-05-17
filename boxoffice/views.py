from django.shortcuts import render
from django.http import HttpResponse
from .reports import generate_ticket_pdf
from .models import Ticket, Order


def boxoffice(request):
    order = Order.objects.get(pk=1)
    return generate_ticket_pdf(request, order)


def basket(request):
    pass


def validate_ticket(request, ticket_id):
    # Get ticket information
    ticket = Ticket.objects.get(ticket_id=ticket_id)

    return HttpResponse(f"<h1>{str(ticket.date)}</h1>")
