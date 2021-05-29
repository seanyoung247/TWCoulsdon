""" Defines forms for the boxoffice app's models """
from django import forms
from .models import Order


# Largely based on the boutique ado project form, with the removal of delivery
# information as tickets are delivered electronically.
class OrderForm(forms.ModelForm):
    """ Defines the form for the order model """
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',)

    def __init__(self, *args, **kwargs):
        """ Creates placeholders and classes for form. """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Your Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
        }
        help_text = {
            'email': "Your tickets will be sent to this address",
            'phone_number': 'We may need to contact you on this number, \
                                for instance if a show is cancelled.',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            if field in help_text:
                self.fields[field].help_text = help_text[field]

            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
