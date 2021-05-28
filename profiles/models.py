""" Defines the profile app's models """
# pylint: disable=E5142
# Importing user model requried for link in user profile
# pylint: disable=W0613
# Unused argument: Arguments are django pattern

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile """
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
