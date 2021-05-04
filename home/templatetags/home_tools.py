from django import template

register = template.Library()

@register.filter(name='iter_range')
def iter_range(items):
    return range(0,items)