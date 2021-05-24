""" Unit tests for tickets.py """
# pylint: disable=R0902
# Creating lots of member attributes for setup of tests

import json

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from events.models import Event, EventDate, Venue
from .models import TicketType, Ticket, Order
from .tickets import (check_ticket_available, check_basket_availability,
                        check_order_availabillity, create_tickets_for_order,
                        TicketsNotAvailable, EmptyOrder)


class TestTestCheckAvailability(TestCase):
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
        self.ticket_types.append(TicketType.objects.create(
            name = "test2", display_name = "Test Ticket2"))

        # Create tickets for event_two
        for date in self.dates_event_two:
            for _ in range(0, 5):
                Ticket.objects.create(
                    order = self.order, type = self.ticket_types[0],
                    event = self.event_two, date = date
                )

        # Create some test baskets
        self.good_basket = {}   # All good
        self.bad_basket = {}    # All bad
        self.mixed_basket = {}  # Some good, some bad
        # Create a basket with available tickets
        for date in self.dates_event_two:
            self.good_basket[date.id] = {
                self.ticket_types[0].id: 2,
                self.ticket_types[1].id: 2,
            }

        # Create a basket with unavailable tickets
        for date in self.dates_event_two:
            self.bad_basket[date.id] = {
                self.ticket_types[0].id: 4,
                self.ticket_types[1].id: 4,
            }
        # Create a basket with a mix of available and unavailable tickets
        self.mixed_basket[self.date_event_one.id] = {
            self.ticket_types[0].id: 4,
            self.ticket_types[1].id: 4,
        }
        for date in self.dates_event_two:
            self.mixed_basket[date.id] = {
                self.ticket_types[0].id: 4,
                self.ticket_types[1].id: 4,
            }


    def test_check_ticket_available(self):
        """ Tests correct returns from check_ticket_available """
        # Check correct return if no tickets have been bought
        self.assertTrue(check_ticket_available(self.date_event_one, 2))
        # Check correct return if tickets have been bought, but enough are left
        self.assertTrue(check_ticket_available(self.dates_event_two[0],2))
        # Check correct return if required and remaining are the same
        self.assertTrue(check_ticket_available(self.dates_event_two[0],5))
        # Check correct return if there are not enough tickets
        self.assertFalse(check_ticket_available(self.dates_event_two[0],8))


    def test_check_basket_availability(self):
        """ Tests correct returns from check_basket_availability """
        # Check correct return from a basket with availability
        self.assertTrue(check_basket_availability(self.good_basket))
        # Check correct return from a basket with no availability
        self.assertRaises(TicketsNotAvailable, check_basket_availability,
                            self.bad_basket)
        # Check correct return from a basket with some availability
        self.assertRaises(TicketsNotAvailable, check_basket_availability,
                            self.mixed_basket)
        try:
            check_basket_availability(self.mixed_basket)
        except TicketsNotAvailable as error:
            self.assertEqual(error.date_id, self.dates_event_two[0].id)


    def test_check_order_availabillity(self):
        """ Tests correct returns from check_order_availabillity """
        # Check an order with availability
        self.order.original_basket = json.dumps(self.good_basket)
        self.assertTrue(check_order_availabillity(self.order))
        # Check an order with no availability
        self.order.original_basket = json.dumps(self.bad_basket)
        self.assertRaises(TicketsNotAvailable, check_order_availabillity,
                            self.order)
        # Check an order with some availability
        self.order.original_basket = json.dumps(self.mixed_basket)
        self.assertRaises(TicketsNotAvailable, check_order_availabillity,
                            self.order)


class TestTicketCreation(TestCase):
    """ Tests that tickets are created properly from an order """
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
        self.ticket_types.append(TicketType.objects.create(
            name = "test2", display_name = "Test Ticket2"))


    def test_simple_order(self):
        """
        Tests that tickets are created correctly for an order
        with tickets of a single date, event, and type
        """
        # Create a simple basket
        basket = {}
        basket[self.date_event_one.id] = {
            self.ticket_types[0].id: 2
        }
        self.order.original_basket = json.dumps(basket)
        create_tickets_for_order(self.order)

        # Check there are the right number of tickets for each type and date
        ticket_count = Ticket.objects.filter(
            date=self.date_event_one, type=self.ticket_types[0]).count()
        self.assertEqual(ticket_count, 2)
        # Check that there aren't any incorrect tickets
        ticket_count = Ticket.objects.filter(
            date=self.date_event_one, type=self.ticket_types[1]).count()
        self.assertEqual(ticket_count, 0)
        ticket_count = Ticket.objects.filter(event=self.event_two).count()
        self.assertEqual(ticket_count, 0)


    def test_multiple_type_order(self):
        """
        Tests that tickets are created correctly for an order
        with tickets of a single date and event but multiple types
        """
        basket = {}
        basket[self.date_event_one.id] = {
            self.ticket_types[0].id: 4,
            self.ticket_types[1].id: 6,
        }
        self.order.original_basket = json.dumps(basket)
        create_tickets_for_order(self.order)
        # Check there are the right number of tickets for each type and date
        ticket_count = Ticket.objects.filter(
            date=self.date_event_one, type=self.ticket_types[0].id).count()
        self.assertEqual(ticket_count, 4)
        ticket_count = Ticket.objects.filter(
            date=self.date_event_one, type=self.ticket_types[1].id).count()
        self.assertEqual(ticket_count, 6)
        # Check that there aren't any incorrect tickets
        ticket_count = Ticket.objects.filter(event=self.event_two).count()
        self.assertEqual(ticket_count, 0)


    def test_multiple_date_order(self):
        """
        Tests that tickets are created correctly for an order
        with tickets of a single event but multiple dates and types
        """
        basket = {}
        for date in self.dates_event_two:
            basket[date.id] = {
                self.ticket_types[0].id: 2,
                self.ticket_types[1].id: 4,
            }
        self.order.original_basket = json.dumps(basket)
        create_tickets_for_order(self.order)
        # Check there are the right number of tickets for each type and date
        for date in self.dates_event_two:
            ticket_count = Ticket.objects.filter(
                date=date, type=self.ticket_types[0].id).count()
            self.assertEqual(ticket_count, 2)
            ticket_count = Ticket.objects.filter(
                date=date, type=self.ticket_types[1].id).count()
            self.assertEqual(ticket_count, 4)
        # Check that there aren't any incorrect tickets
        ticket_count = Ticket.objects.filter(event=self.event_one).count()
        self.assertEqual(ticket_count, 0)
        ticket_count = Ticket.objects.filter(event=self.event_two).count()
        self.assertEqual(ticket_count, 12)


    def test_multiple_event_order(self):
        """
        Tests that tickets are created correctly for an order
        with tickets of multiple events, dates, and types
        """
        basket = {}
        basket[self.date_event_one.id] = {
            self.ticket_types[0].id: 4,
            self.ticket_types[1].id: 6,
        }
        for date in self.dates_event_two:
            basket[date.id] = {
                self.ticket_types[0].id: 2,
                self.ticket_types[1].id: 4,
            }
        self.order.original_basket = json.dumps(basket)
        create_tickets_for_order(self.order)
        ticket_count = Ticket.objects.filter(event=self.event_one).count()
        self.assertEqual(ticket_count, 10)
        ticket_count = Ticket.objects.filter(event=self.event_two).count()
        self.assertEqual(ticket_count, 12)


    def test_fails_on_empty(self):
        """
        Tests that ticket creation fails if order basket is empty
        """
        self.order.original_basket = json.dumps({})
        self.assertRaises(EmptyOrder, create_tickets_for_order, self.order)
        self.order.original_basket = ""
        self.assertRaises(EmptyOrder, create_tickets_for_order, self.order)


    def test_fails_on_bad_line(self):
        """
        Tests that ticket creation fails if one line is unavailable
        and that no tickets are created
        """
        basket = {}
        basket[self.date_event_one.id] = {
            self.ticket_types[0].id: 2
        }
        basket[self.dates_event_two[0].id] = {
            self.ticket_types[0].id: 12
        }
        self.order.original_basket = json.dumps(basket)
        self.assertRaises(TicketsNotAvailable, create_tickets_for_order, self.order)
        # Check no tickets created
        ticket_count = Ticket.objects.filter(event=self.event_one).count()
        self.assertEqual(ticket_count, 0)
        ticket_count = Ticket.objects.filter(event=self.event_two).count()
        self.assertEqual(ticket_count, 0)

    def test_fails_on_bad_order(self):
        """
        Tests that ticket creation fails if all lines are unavailable
        and that no tickets are created
        """
        basket = {}
        basket[self.date_event_one.id] = {
            self.ticket_types[0].id: 5,
            self.ticket_types[1].id: 6,
        }
        for date in self.dates_event_two:
            basket[date.id] = {
                self.ticket_types[0].id: 11,
                self.ticket_types[1].id: 12,
            }
        self.order.original_basket = json.dumps(basket)
        self.assertRaises(TicketsNotAvailable, create_tickets_for_order, self.order)
        # Check no tickets created
        ticket_count = Ticket.objects.filter(event=self.event_one).count()
        self.assertEqual(ticket_count, 0)
        ticket_count = Ticket.objects.filter(event=self.event_two).count()
        self.assertEqual(ticket_count, 0)
