""" Defines tests for the the  """
# pylint: disable=E5142
# I need to import user for testing. I don't need get_user_model() in this case

from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from events.models import Event, EventDate
from profiles.models import UserProfile

from .models import TicketType, Ticket, Order


class TestTicketType(TestCase):
    """ Tests the TicketType model """
    def test_price_defaults_to_zero(self):
        """ Ensures price is given the correct default value """
        ticket_type = TicketType.objects.create(name="test", display_name="Test Ticket")
        self.assertEqual(ticket_type.price, 0)

    def test_string_returns_name(self):
        """ Ensures price is given the correct default value """
        ticket_type = TicketType.objects.create(name="test")
        self.assertEqual(str(ticket_type), "test")


class TestTicket(TestCase):
    """ Tests the Ticket model """
    def setUp(self):
        self.user = User.objects.create_user(
            'Test User', 'test@email.com', 'testpassword')
        self.user_profile = UserProfile.objects.get(user=self.user)

        self.event = Event.objects.create(
            title = "Test Event",
            description = "Test Event"
        )
        self.date = EventDate.objects.create(
            event = self.event, date = timezone.now())

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

    def test_all_fields_required(self):
        """ Ensures Ticket won't be created without all fields being filled """
        with transaction.atomic():
            self.assertRaises(IntegrityError, Ticket.objects.create)

    def test_ticket_unique_id(self):
        """ Tests that two identical tickets will have different identifiers """
        ticket = Ticket.objects.create(
            order = self.order, type = self.ticket_type,
            event = self.event, date = self.date
        )
        self.assertNotEqual(ticket.ticket_id, None)
        self.assertNotEqual(ticket.ticket_id, '')
        self.assertNotEqual(ticket.ticket_id, self.ticket.ticket_id)

    def test_string_returns_id(self):
        """ Ensures the __str__ method returns the unique ticket id """
        self.assertEqual(str(self.ticket.ticket_id), self.ticket.ticket_id)


class TestOrder(TestCase):
    """ Tests the Order model """
    def setUp(self):
        self.user = User.objects.create_user(
        'Test User', 'test@email.com', 'testpassword')
        self.user_profile = UserProfile.objects.get(user=self.user)

        self.event = Event.objects.create(
            title = "Test Event",
            description = "Test Event"
        )
        self.date = EventDate.objects.create(
            event = self.event, date = timezone.now())

        self.order = Order.objects.create(
            user_profile = self.user_profile,
            full_name = "Test User",
            email = self.user.email
        )
        self.ticket_type = TicketType.objects.create(
            name = "test",
            display_name = "Test Ticket",
            price = 10.00
        )

    def tearDown(self):
        self.user.delete()

    def test_string_returns_order_number(self):
        """ Tests that the __str__ method returns  """
        self.assertEqual(str(self.order), self.order.order_number)

    def test_order_number_unique(self):
        """ Tests that identical orders produce unqiue order numbers """
        order = Order.objects.create(
            user_profile = self.user_profile,
            full_name = "Test User",
            email = self.user.email
        )
        self.assertNotEqual(self.order.order_number, order.order_number)

    def test_order_total_updated(self):
        """
        Tests that the custom signals are triggered and order totals updated as
        tickets are added and removed.
        """
        self.assertEqual(self.order.order_total, 0)
        Ticket.objects.create(
            order = self.order, type = self.ticket_type,
            event = self.event, date = self.date
        )
        self.assertEqual(self.order.order_total, 10.00)
        ticket = Ticket.objects.create(
            order = self.order, type = self.ticket_type,
            event = self.event, date = self.date
        )
        self.assertEqual(self.order.order_total, 20.00)
        ticket.delete()
        self.assertEqual(self.order.order_total, 10.00)
