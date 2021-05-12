""" Defines tests for the the  """

from unittest import mock
from django.test import TestCase
from django.db import IntegrityError
from events.models import Event, EventDate
from profiles.models import UserProfile

from .models import TicketType, Ticket, Order


class TestTicketType(TestCase):
    """ Tests the TicketType model """
    def test_price_defaults_to_zero(self):
        """ Ensures price is given the correct default value """
        type = TicketType.objects.create(name="test", display_name="Test Ticket")
        self.assertEqual(type.price, 0)

    def test_string_returns_name(self):
        """ Ensures price is given the correct default value """
        type = TicketType.objects.create(name="test")
        self.assertEqual(str(type), "test")


class TestTicket(TestCase):
    """ Tests the Ticket model """
    pass


class TestOrder(TestCase):
    pass
