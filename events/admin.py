from django.contrib import admin
from .models import ShowType, EventDate, Venue, Event, Image


class ShowTypeAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )
    

class EventDateAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'date',
    )

    ordering = ('event',)
    

class VenueAdmin(admin.ModelAdmin):
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
    )
    

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'tagline',
        'description',
        'content',
        'type',
        'venue',
        'title_image'
    )
    

class ImageAdmin(admin.ModelAdmin):
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