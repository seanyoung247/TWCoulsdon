from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter(name='in_the_future')
def in_the_future(date):
    if date:
        return date > timezone.now()
    return False