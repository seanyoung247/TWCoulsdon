""" Core site templatetags """
from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='iter_range')
def iter_range(items):
    """ returns a zero based range list for iteration in templates """
    return range(0,items)


@register.filter(name='check_image')
def check_image(image):
    """ Checks an image is defined or replaces it with the default no image """
    if image:
        return image.url

    return settings.NO_IMAGE
