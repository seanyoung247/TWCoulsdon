from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class TestUserProfile(TestCase):
    """ Tests the userprofile model """
    def test_auto_creation(self):
        """
        Tests that the user profile is automatically created when the user
        account is created
        """
        pass