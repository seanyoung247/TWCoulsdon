""" Defines helper functions for debugging """
from django.conf import settings

def debug_print(msg):
    """ Prints to the console only if debugging """
    if settings.DEBUG: print(msg)
