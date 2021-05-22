""" Tests the home app's models """
from django.test import TestCase
from .models import Category, Page


class TestCategory(TestCase):
    """ Tests the Category model and members """
    def setUp(self):
        self.category = Category.objects.create(
            name="test",
            display_name="Test Category"
        )

    def test_string_returns_name(self):
        """ Tests that the __str__ method returns the category name """
        self.assertEqual(str(self.category), "test")

    def test_display_name(self):
        """ Tests that the correct display name is returned """
        self.assertEqual(self.category.get_display_name(), "Test Category")

    def test_slug_generation(self):
        """ Tests that the URL slug is created properly """
        self.assertEqual(self.category.slug, "test")


class TestPage(TestCase):
    """ Tests that Page model and members """
    def setUp(self):
        self.category = Category.objects.create(
            name="test",
            display_name="Test Category"
        )
        self.page = Page.objects.create(
            category=self.category,
            title="Test Page",
            description="This is a test page",
            content="<h1>Test Content</h1><p>This is a test page</p>"
        )

    def test_string_returns_title(self):
        """ Tests that the __str__ method returns the category title """
        self.assertEqual(str(self.page), "Test Page")

    def test_slug_generation(self):
        """ Tests that the URL slug is created properly """
        self.assertEqual(self.page.slug, "test-page")

