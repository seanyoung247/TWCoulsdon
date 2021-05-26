""" Defines the user profile form """
# pylint: disable=E5142
# Importing user model to fill attributes

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserInfoForm(forms.ModelForm):
    """ Exposes some of the user models fields for updating """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        """ Initialises the user form """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = False


class UserProfileForm(forms.ModelForm):
    """ Creates a form for the UserProfile model """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ Initialises the user profile form """
        super().__init__(*args, **kwargs)
        self.fields['default_phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['default_phone_number'].label = False
