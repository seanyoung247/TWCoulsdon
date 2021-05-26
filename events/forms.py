""" Defines the forms used by the events app """

from django import forms
from .models import EventDate, Event, Venue, Image


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


class ImageForm(forms.modelForm):
    """ Creates a form to create and update images """
    class Meta:
        model = Image
        exclude = ('event',)

    def __init__(self, *args, **kwargs):
        """ Initialises the EventDate form """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'description': 'Description',
            'image': 'Image',
        }

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
