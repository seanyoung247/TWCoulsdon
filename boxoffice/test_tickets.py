""" Unit tests for tickets.py """
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from events.models import Event, EventDate, Venue
from .models import TicketType, Ticket, Order
from .tickets import (check_ticket_available, check_basket_availability,
                        check_order_availabillity, create_tickets,
                        Tickets_Not_Available)


class TestCheckAvailability(TestCase):
    """ Tests the various ticket availability functions """
    def setUp(self):
        self.venue = Venue.objects.create(
            name = "Test Venue",
            capacity = 10
        )
        self.event_one = Event.objects.create(
            title = "Test Event",
            description = "Test Event",
            venue = self.venue
        )
        self.event_two = Event.objects.create(
            title = "Test Event",
            description = "Test Event",
            venue = self.venue
        )
        self.date_event_one = EventDate.objects.create(
            event = self.event_one, date = timezone.now() + timedelta(days=10))

        self.dates_event_two = []
        self.dates_event_two.append(EventDate.objects.create(
            event = self.event_two, date = timezone.now() + timedelta(days=15)))
        self.dates_event_two.append(EventDate.objects.create(
            event = self.event_two, date = timezone.now() + timedelta(days=20)))

        self.order = Order.objects.create(
            full_name = "Test User",
            email = "Test@email.com",
            phone_number = "01234567890",
        )
        self.ticket_types = []
        self.ticket_types.append(TicketType.objects.create(
            name = "test", display_name = "Test Ticket"))

        # Create tickets for event_two
        for date in self.dates_event_two:
            for i in range(0, 5):
                Ticket.objects.create(
                    order = self.order, type = self.ticket_type,
                    event = self.event_two, date = date
                )

        # Create some test baskets



    def test_check_ticket_available(self):
        # Check correct return if no tickets have been bought
        self.assertTrue(check_ticket_available(self.date_event_one, 2))
        # Check correct return if tickets have been bought, but enough are left
        self.assertTrue(check_ticket_available(self.dates_event_two[0],2))
        # Check correct return if required and remaining are the same
        self.assertTrue(check_ticket_available(self.dates_event_two[0],5))
        # Check correct return if there are not enough tickets
        self.assertFalse(check_ticket_available(self.dates_event_two[0],8))






