""" Defines inter-model signalling for the boxoffice app """
# pylint: disable=W0613
# Django function pattern can't be changed

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Ticket

@receiver(post_save, sender=Ticket)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on Ticket update/create
    """
    instance.order.update_total()

@receiver(post_delete, sender=Ticket)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on Ticket delete
    """
    instance.order.update_total()
