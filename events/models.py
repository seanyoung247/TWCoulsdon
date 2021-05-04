""" Defines database models for the Events app """
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField
from tinymce.models import HTMLField
from easy_thumbnails.fields import ThumbnailerImageField
from embed_video.fields import EmbedVideoField
from home.models import SlugModel

class ShowType(models.Model):
    """ Defines the types of Events """
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        """ Returns the ShowType's display name """
        return self.display_name


class EventDate(models.Model):
    """ Defines an individual Event performance date """
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.date.strftime('%d/%m/%Y, %H:%M')


class Venue(models.Model):
    """ Provides information on a Venue used by Events """
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
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Event(SlugModel):
    """ Defines the information and relationships for events """
    title = models.CharField(max_length=50, null=False, blank=False)
    author = models.CharField(max_length=64, null=True, blank=True)
    tagline = models.CharField(max_length=256, null=True, blank=True)
    description = HTMLField()
    type = models.ForeignKey('ShowType', null=True, blank=True, on_delete=models.SET_NULL)
    venue = models.ForeignKey('Venue', null=True, blank=True, on_delete=models.SET_NULL)
    title_image = models.ForeignKey('Image', related_name='+',
        null=True, blank=True, on_delete=models.SET_NULL
    )
    content = EmbedVideoField(null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Do we need to generate a slug?
        if not self.pk:
            self._generate_slug(Event, self.title)

        super().save(*args, **kwargs)


class Image(models.Model):
    """ Stores information on uploaded images """
    event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256, null=True, blank=True)
    image = ThumbnailerImageField(null=True, blank=True)

    def __str__(self):
        return self.name
