""" App configuration """
from django.apps import AppConfig


class BoxofficeConfig(AppConfig):
    """ App configuration """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boxoffice'

    def ready(self):
        import boxoffice.signals
