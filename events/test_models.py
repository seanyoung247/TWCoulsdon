""" Tests the event apps models """
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from .models import ShowType, EventDate, Venue, Event


class TestShowType(TestCase):
    """ Tests the ShowType model and class members """

    def test_display_name_defaults_blank(self):
        """ Ensures display name is created with correct defaults """
        type = ShowType.objects.create(name="test")
        self.assertTrue(type.display_name is None)

    def test_string_method_returns_name(self):
        """ Ensures the ShowType __str__ method returns name field """
        type = ShowType.objects.create(name="test")
        self.assertEqual(str(type), "test")

    def test_display_name(self):
        """ Ensures the ShowType display_name field is set and returned """
        type = ShowType.objects.create(name="test", display_name="Test Type")
        self.assertEqual(type.get_display_name(), "Test Type")


class TestEventDate(TestCase):
    """ Tests the EventDate model and class members """
    def setUp(self):
        """ Sets up common test objects """
        Event.objects.create(title="Test Event")

    def test_date_required(self):
        """ Tests that the date field is required to create an EventDate """
        event = Event.objects.get(title="Test Event")
        self.assertRaises(IntegrityError, EventDate.objects.create, event=event)

    def test_event_required(self):
        """ Tests the the event field is required to create an EventDate """
        self.assertRaises(IntegrityError, EventDate.objects.create, date=timezone.now())

    def test_string_returns_date(self):
        """ Tests that the __str__ method returns the string date and time """
        event = Event.objects.get(title="Test Event")
        str_date = '10/04/2021, 10:30'
        date = EventDate.objects.create(
            event=event,
            date=timezone.make_aware(datetime.strptime(str_date, '%d/%m/%Y, %H:%M'))
        )
        self.assertEqual(str(date), str_date)


class TestVenue(TestCase):
    """ Tests the venue model and class members """
    def test_string_method_returns_name(self):
        """ Ensures the ShowType __str__ method returns name field """
        venue = Venue.objects.create(name="Test Venue")
        self.assertEqual(str(venue), "Test Venue")


class TestEvent(TestCase):
    """ Tests the Event model and class members """
    def test_string_returns_title(self):
        event = Event.objects.create(title="Test Event")
        self.assertEqual(str(event), "Test Event")

    def test_slug_generation(self):
        event = Event.objects.create(title="Test Event")
        self.assertEqual(event.slug, "test-event")
        event = Event.objects.create(title="Test Event")
        self.assertEqual(event.slug, "test-event-1")







