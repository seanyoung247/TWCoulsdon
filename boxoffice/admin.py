""" Registers boxoffic models with django admin """
from django.contrib import admin
from .models import TicketType, Ticket, Order


class TicketTypeAdmin(admin.ModelAdmin):
    """ Registers TicketType model with django admin """
    list_display = (
        'name',
        'display_name',
        'price',
    )


class TicketAdmin(admin.ModelAdmin):
    """ Registers Ticket model with django admin """
    list_display = (
        'ticket_id',
        'order',
        'type',
        'event',
        'date',
    )

    ordering = ('event',)


class OrderAdmin(admin.ModelAdmin):
    """ Registers order model with django admin """
    list_display = (
        'order_number',
        'user_profile',
        'date',
        'original_bag',
        'stripe_pid',
        'full_name',
        'email',
        'order_total',
        'grand_total',
        'phone_number',
    )

    ordering = ('date',)


admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Order, OrderAdmin)
