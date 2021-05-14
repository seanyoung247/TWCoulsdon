""" Defines helper functions for debugging """
from django.conf import settings

debug_print = lambda msg: print(msg) if settings.DEBUG else None
