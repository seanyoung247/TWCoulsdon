from django.contrib import admin
from .models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    """ Registers Category model with Django admin """
    list_display = (
        'name',
        'display_name',
        'title_page',
    )


class PageAdmin(admin.ModelAdmin):
    """ Registers Page model with Django admin """
    list_display = (
        'category',
        'title',
        'description',
        'content',
        'image',
    )

    ordering = ('event',)