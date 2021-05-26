""" Defines the forms used by the events app """

from django import forms
from .models import ShowType, EventDate, Event, Venue, Image


class EventDateForm(forms.modelForm):
    """ Creates a form to create and update event dates """
    class Meta:
        model = EventDate
        # Event is generated automatically on creation
        exclude = ('event',)

    def __init__(self, *args, **kwargs):
        """ Initialises the EventDate form """
        super().__init__(*args, **kwargs)

        self.fields['date'].widget.attrs['placeholder'] = 'Date'
        self.fields[field].label = False