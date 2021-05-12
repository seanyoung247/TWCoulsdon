""" Tests the home app's views """
from django.test import TestCase
from .models import Category, Page
from events.models import Event


class TestHomeViews(TestCase):
    """ Tests the home app views """
    def setUp(self):
        self.category = Category.objects.create(
            name = 'test',
            display_name = f'Test Category'
        )

        self.page = Page.objects.create(
            category = self.category,
            title = 'Test Page',
            description = 'This is a test page',
            content = '<h1>Test Page</h1><p>This is test page number</p>'
        )
        self.category.title_page = self.page
        self.category.save()

        self.event = Event.objects.create(
            title = 'Test Event'
        )

    def test_landing_page(self):
        """ Tests loading the landing page """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_category_page(self):
        """ Tests loading a category page """
        response = self.client.get(f'/twc/{self.category.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/page.html')

    def test_content_page(self):
        """ Tests loading a content page """
        response = self.client.get(f'/twc/{self.category.slug}/{self.page.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/page.html')

