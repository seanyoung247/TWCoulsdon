from django.db import models

from datetime import datetime
from tinymce.models import HTMLField
from django_countries.fields import CountryField
from easy_thumbnails.fields import ThumbnailerImageField
from embed_video.fields import EmbedVideoField
from django.utils.text import slugify
import itertools


class ShowType(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name
    
        
class EventDate(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    date = models.DateTimeField()
    #TODO: Add Capacity
    
    def __str__(self):
        return self.date.strftime('%d/%m/%Y, %H:%M')


class Venue(models.Model):
    name = models.CharField(max_length=50)
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
    slug = models.SlugField(max_length=64, editable=False, null=False, blank=False, unique=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    author = models.CharField(max_length=64, null=True, blank=True)
    tagline = models.CharField(max_length=256, null=True, blank=True)
    description = HTMLField()
    type = models.ForeignKey('ShowType', null=True, blank=True, on_delete=models.SET_NULL)
    venue = models.ForeignKey('Venue', null=True, blank=True, on_delete=models.SET_NULL)
    title_image = models.ForeignKey('Image', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    content = EmbedVideoField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __generate_slug(self):
        """ Generates a URL slug from the event title """
        # Based on code from: 
        # https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/
        
        # Generate a candidate for the slug
        max_length = self._meta.get_field('slug').max_length
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        # Ensure that the candidate is unique
        for i in itertools.count(1):
            if not Event.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate
    
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        # Do we need to generate a slug?
        if not self.pk:
            self.__generate_slug()
        
        super().save(*args, **kwargs)
    
    
class Image(models.Model):    
    event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256, null=True, blank=True)
    image = ThumbnailerImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    