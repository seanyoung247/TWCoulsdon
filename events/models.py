from django.db import models

from datetime import datetime
from tinymce.models import HTMLField
from django_countries.fields import CountryField


class ShowType(models.Model):
    name = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name
    
        
class EventDate(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def __str__(self):
        return self.date.strftime('%d/%m/%Y, %H:%M')


class Venue(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=True, blank=True)
    
    def __str__(self):
        return self.name
        
    
class Event(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    tagline = models.CharField(max_length=256)
    description = HTMLField()
    type = models.ForeignKey('ShowType', null=True, blank=True, on_delete=models.SET_NULL)
    venue = models.ForeignKey('Venue', null=True, blank=True, on_delete=models.SET_NULL)
    title_image = models.ForeignKey('Image', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.title
        
    
class Image(models.Model):
    event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    