from datetime import datetime, timedelta

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
        self.userProfile = UserProfile.objects.get(user=self.user)
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
            user_profile = self.userProfile,
            full_name = "Test User",
            email = self.user.email
        )
        self.ticketType = TicketType.objects.create(
            name = "test", display_name = "Test Ticket")
        self.ticket = Ticket.objects.create(
            order = self.order, type = self.ticketType,
            event = self.event, date = self.date
        )

    def tearDown(self):
        self.user.delete()


    def test_get_available_tickets_for_date(self):
        """ Ensures the correct number of tickets are returned for dates """
        count = get_available_tickets_for_date(self.date)
        # Venue = 10 seats, 1 - ticket == 9 left
        self.assertEqual(count, 9)
        # Create enough tickets to sell-out date
        for i in range(1,10):
            Ticket.objects.create(
                order = self.order, type = self.ticketType,
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
        Ticket.objects.create(
            order = self.order, type = self.ticketType,
            event = self.event, date = past_date
        )
        count = get_available_tickets_for_event(self.event)
        self.assertEqual(count, 19)
        # Add a ticket to the future date to ensure the new
        # total is correctly returned
        Ticket.objects.create(
            order = self.order, type = self.ticketType,
            event = self.event, date = future_date
        )
        count = get_available_tickets_for_event(self.event)
        self.assertEqual(count, 18)

