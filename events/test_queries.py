""" Defines tests for the event app views """
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from .models import ShowType, EventDate, Venue, Event
from .queries import (query_events_by_first_date, query_events_by_last_date,
                      query_events_by_text_search, query_events_by_type,
                      query_events, get_future_events, get_event_dates,
                      get_remaining_event_dates)


class TestEventsQueries(TestCase):
    """ Tests event querying """
    def setUp(self):
        type_show = ShowType.objects.create(
            name="show",
            display_name="Test Show"
        )
        type_film = ShowType.objects.create(
            name="film",
            display_name="Test Film"
        )
        venue = Venue.objects.create(name="Test Venue")
        self.event_show1 = Event.objects.create(
            title="Test_Show-1",
            description="<h1>Test Show 1</h1><p>This is a test event</p>",
            type=type_show,
            venue=venue
        )
        self.event_show2 = Event.objects.create(
            title="Test_Show-2",
            description="<h1>Test Show 2</h1><p>This is a test event</p>",
            type=type_show,
            venue=venue
        )
        self.event_film = Event.objects.create(
            title="Test_Film",
            description="<h1>Test Film</h1><p>This is a test event</p>",
            type=type_film
        )
        # Always in the past
        self.past_date = EventDate.objects.create(
            event=self.event_show1,
            date=(timezone.now() - timedelta(days=10))
        )
        # Always in the future
        self.future_date = EventDate.objects.create(
            event=self.event_show2,
            date=(timezone.now() + timedelta(days=10))
        )


    def test_query_events_by_first_date(self):
        """ Tests that events later than date are returned """
        events = list(query_events_by_first_date(Event.objects.all(), timezone.now()))
        self.assertTrue(self.event_show2 in events)
        self.assertFalse(self.event_show1 in events)


    def test_query_events_by_last_date(self):
        """ Tests that events earlier than date are returned """
        events = list(query_events_by_last_date(Event.objects.all(), timezone.now()))
        self.assertFalse(self.event_show2 in events)
        self.assertTrue(self.event_show1 in events)


    def test_query_events_by_text_search(self):
        """ Tests that events conforming to string queries are returned """
        events = list(query_events_by_text_search(Event.objects.all(), 'Film'))
        self.assertTrue(self.event_film in events)
        self.assertFalse(self.event_show1 in events)


    def test_query_events_by_type(self):
        """ Tests events of specific types are returned """
        events = list(query_events_by_type(Event.objects.all(), 'show'))
        self.assertTrue(self.event_show1 in events)
        self.assertTrue(self.event_show2 in events)
        self.assertFalse(self.event_film in events)
        events = list(query_events_by_type(Event.objects.all(), 'film'))
        self.assertFalse(self.event_show1 in events)
        self.assertFalse(self.event_show2 in events)
        self.assertTrue(self.event_film in events)


    def test_query_events(self):
        """ Tests the correct events are returned from compound queries """
        query_list = {
            'q': 'test',
            'type': 'show'
        }
        results = query_events(query_list)
        events = list(results['events'])
        showcase = list(results['showcase_events'])
        self.assertTrue(self.event_show1 in events)
        self.assertTrue(self.event_show2 in showcase)
        self.assertFalse(self.event_film in events)


    def test_get_future_events(self):
        """ Tests only events in the future are returned """
        events = list(get_future_events())
        self.assertFalse(self.event_show1 in events)
        self.assertTrue(self.event_show2 in events)


    def test_get_event_dates(self):
        """ Tests that all an events dates can be returned """
        date = EventDate.objects.create(
            event=self.event_show2,
            date=(timezone.now() + timedelta(days=10))
        )
        dates = list(get_event_dates(self.event_show2))
        self.assertTrue(date in dates)
        self.assertTrue(self.future_date in dates)
        self.assertFalse(self.past_date in dates)


    def test_get_remaining_event_dates(self):
        """ Tests that only remaining dates are returned """
        date = EventDate.objects.create(
            event=self.event_show2,
            date=(timezone.now() - timedelta(days=10))
        )
        dates = list(get_remaining_event_dates(self.event_show2))
        self.assertFalse(date in dates)
        self.assertTrue(self.future_date in dates)
        self.assertFalse(self.past_date in dates)
