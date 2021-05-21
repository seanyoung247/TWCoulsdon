from django import forms
from .models import Order


# Largely based on the boutique ado project form, with the removal of delivery
# information as tickets are delivered electronically.
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email','phone_number',)

    def __init__(self, *args, **kwargs):
        """ Creates placeholders and classes for form. """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            placeholder = f'{placeholders[field]} *'
        else:
            placeholder = placeholders[field]

        self.fields[field].widget.attrs['placeholder'] = placeholder
        self.fields[field].widget.attrs['class'] = 'stripe-style-input'
        self.fields[field].label = False
