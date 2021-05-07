""" Template tags for the event app """

from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='in_the_future')
def in_the_future(date):
    """ Returns true if date is in the future """
    if date:
        return date > timezone.now()
    return False
