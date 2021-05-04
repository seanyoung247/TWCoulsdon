""" Registers models with django admin """
from django.contrib import admin
from .models import ShowType, EventDate, Venue, Event, Image


class ShowTypeAdmin(admin.ModelAdmin):
    """ Registers ShowType model with Django admin """
    list_display = (
        'display_name',
        'name',
    )


class EventDateAdmin(admin.ModelAdmin):
    """ Registers EventDate model with Django admin """
    list_display = (
        'event',
        'date',
    )

    ordering = ('event',)


class VenueAdmin(admin.ModelAdmin):
    """ Registers Venue model with Django admin """
    list_display = (
        'name',
        'image',
        'description',
        'email',
        'phone_number',
        'street_address1',
        'street_address2',
        'town_or_city',
        'county',
        'postcode',
        'country',
        'longitude',
        'latitude',
    )


class EventAdmin(admin.ModelAdmin):
    """ Registers Event model with Django admin """
    list_display = (
        'title',
        'author',
        'tagline',
        'description',
        'content',
        'type',
        'venue',
        'title_image',
    )


class ImageAdmin(admin.ModelAdmin):
    """ Registers Image model with Django admin """
    list_display = (
        'event',
        'name',
        'description',
        'image',
    )

    ordering = ('event',)


admin.site.register(ShowType, ShowTypeAdmin)
admin.site.register(EventDate, EventDateAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Image, ImageAdmin)
