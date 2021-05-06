from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='iter_range')
def iter_range(items):
    return range(0,items)


@register.filter(name='check_image')
def check_image(image):
    if image:
        return image.url
    else:
        return settings.NO_IMAGE