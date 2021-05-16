""" Defines tests for the event app views """
from datetime import timedelta
from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from .models import ShowType, EventDate, Venue, Event


class TestEventsViews(TestCase):
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
        for i in range(3,settings.RESULTS_PER_PAGE*2):
            Event.objects.create(
                title=f"Test_Show-{i}",
                description=f"<h1>Test Show {i}</h1><p>This is a test event</p>",
                type=type_show,
                venue=venue
            )
        event_show1 = Event.objects.create(
            title="Test_Show-1",
            description="<h1>Test Show 1</h1><p>This is a test event</p>",
            type=type_show,
            venue=venue
        )
        event_show2 = Event.objects.create(
            title="Test_Show-2",
            description="<h1>Test Show 2</h1><p>This is a test event</p>",
            type=type_show,
            venue=venue
        )
        event_film = Event.objects.create(
            title="Test_Film",
            description="<h1>Test Film</h1><p>This is a test event</p>",
            type=type_film
        )
        # Always in the past
        EventDate.objects.create(
            event=event_show1,
            date=(timezone.now() - timedelta(days=10))
        )
        # Always in the future
        EventDate.objects.create(
            event=event_show2,
            date=(timezone.now() + timedelta(days=10))
        )

    def test_get_events_by_type(self):
        """ Tests listing events by type """
        response = self.client.get('/events/?type=show')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events.html')
        self.assertContains(response, 'Test_Show-1')
        self.assertContains(response, 'Test_Show-2')
        self.assertNotContains(response, 'Test_Film')
        response = self.client.get('/events/?type=film')
        self.assertNotContains(response, 'Test_Show-1')
        self.assertNotContains(response, 'Test_Show-2')
        self.assertContains(response, 'Test_Film')

    def test_get_events_by_date(self):
        """ Tests listing events by date """
        str_date = timezone.now().strftime('%Y-%m-%d')
        response = self.client.get(f'/events/?fdate={str_date}')
        self.assertContains(response, 'Test_Show-2')
        self.assertNotContains(response, 'Test_Show-1')
        response = self.client.get(f'/events/?ldate={str_date}')
        self.assertContains(response, 'Test_Show-1')
        self.assertNotContains(response, 'Test_Show-2')

    def test_get_events_by_text_search(self):
        """ Tests listing events by text search """
        response = self.client.get('/events/?q=test')
        self.assertContains(response, 'Test_Show-1')
        self.assertContains(response, 'Test_Show-2')
        self.assertContains(response, 'Test_Film')
        response = self.client.get('/events/?q=Test_Show-1')
        self.assertContains(response, 'Test_Show-1')
        self.assertNotContains(response, 'Test_Show-2')
        self.assertNotContains(response, 'Test_Film')

    def test_events_pagination(self):
        """ Tests retrieving pages of results """
        response = self.client.get('/events/?q=test')
        self.assertNotContains(response, f'Test_Show-{settings.RESULTS_PER_PAGE-1}')
        response = self.client.get('/events/lazy_load/?page=2')
        self.assertContains(response, f'Test_Show-{settings.RESULTS_PER_PAGE-1}')


    def test_event_details_view(self):
        """ Tests retrieving a single event page """
        response = self.client.get('/events/test_show-1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_details.html')
        self.assertContains(response, 'Test_Show-1')


    def test_venue_details_view(self):
        """ Tests retrieving a single venue page """
        response = self.client.get('/events/venue/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/venue_details.html')
        self.assertContains(response, 'Test Venue')
