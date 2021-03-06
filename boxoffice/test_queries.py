""" Tests the database queries in boxoffice.queries """
# pylint: disable=E5142
# I need to import user for testing. I don't need get_user_model() in this case
# pylint: disable=R0902
# Creating lots of member attributes for setup of tests

from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from events.models import Event, EventDate, Venue
from profiles.models import UserProfile
from .models import TicketType, Ticket, Order
from .queries import get_available_tickets_for_date, get_available_tickets_for_event

class TestQueries(TestCase):
    """ Tests the boxoffice app queries """
    def setUp(self):
        self.user = User.objects.create_user(
            'Test User', 'test@email.com', 'testpassword')
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.venue = Venue.objects.create(
            name = "Test Venue",
            capacity = 10
        )
        self.event = Event.objects.create(
            title = "Test Event",
            description = "Test Event",
            venue = self.venue
        )
        self.date = EventDate.objects.create(
            event = self.event, date = timezone.now() + timedelta(days=10))

        self.order = Order.objects.create(
            user_profile = self.user_profile,
            full_name = "Test User",
            email = self.user.email
        )
        self.ticket_type = TicketType.objects.create(
            name = "test", display_name = "Test Ticket")
        self.ticket = Ticket.objects.create(
            order = self.order, type = self.ticket_type,
            event = self.event, date = self.date
        )

    def tearDown(self):
        self.user.delete()


    def test_get_available_tickets_for_date(self):
        """ Ensures the correct number of tickets are returned for dates """
        count = get_available_tickets_for_date(self.date)
        # Venue = 10 seats, 1 - ticket == 9 left
        self.assertEqual(count, 9)
        # Ensure correct value is returned if no tickets have been sold
        self.ticket.delete()
        count = get_available_tickets_for_date(self.date)
        self.assertEqual(count, 10)
        # Create enough tickets to sell-out date
        for _ in range(0,10):
            Ticket.objects.create(
                order = self.order, type = self.ticket_type,
                event = self.event, date = self.date
            )
        # 10 seats - 10 tickets == 0 left
        count = get_available_tickets_for_date(self.date)
        self.assertEqual(count, 0)


    def test_get_available_tickets_for_event(self):
        """ Ensures the correct number of tickets are returned for events """
        count = get_available_tickets_for_event(self.event)
        # 1 date * 10 seats == 10 total seats - 1 ticket = 9 left
        self.assertEqual(count, 9)
        # Test correct value returned with more dates
        past_date = EventDate.objects.create(
            event=self.event,
            date=timezone.now() - timedelta(days=10)
        )
        future_date = EventDate.objects.create(
            event=self.event,
            date=timezone.now() + timedelta(days=5)
        )
        count = get_available_tickets_for_event(self.event)
        # 2 future dates * 10 seats == 20 seats - 1 ticket = 19 left
        self.assertEqual(count, 19)
        # Add a ticket to the past event to ensure the count
        # isn't affected by past events
        ticket1 = Ticket.objects.create(
            order = self.order, type = self.ticket_type,
            event = self.event, date = past_date
        )
        count = get_available_tickets_for_event(self.event)
        self.assertEqual(count, 19)
        # Add a ticket to the future date to ensure the new
        # total is correctly returned
        ticket2 = Ticket.objects.create(
            order = self.order, type = self.ticket_type,
            event = self.event, date = future_date
        )
        count = get_available_tickets_for_event(self.event)
        self.assertEqual(count, 18)
        # Ensure events with no sold tickets return the correct values
        self.ticket.delete()
        ticket1.delete()
        ticket2.delete()
        count = get_available_tickets_for_event(self.event)
        self.assertEqual(count, 20)
