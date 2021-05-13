import uuid
from django.db import models
from django_countries.fields import CountryField
from events.models import Event, EventDate
from profiles.models import UserProfile


class TicketType(models.Model):
    """
    Defines the tickets types (adult, concession)
    """
    name = models.CharField(max_length=50, null=False, blank=False)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """
    Defines a single ticket
    """
    ticket_id = models.CharField(max_length=32, null=False, blank=False, editable=False)
    order = models.ForeignKey('Order', null=False, blank=False,
                                on_delete=models.CASCADE, related_name="tickets")
    type = models.ForeignKey('TicketType', null=False, blank=False, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    date = models.ForeignKey(EventDate, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_id;

    def _generate_ticket_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        # Do we need to generate a unique id?
        if not self.ticket_id:
            self.ticket_id = self._generate_ticket_number()

        super().save(*args, **kwargs)


class Order(models.Model):
    """
    Stores information on individual orders
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True, editable=False)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.order_number

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Recieves the on save/delete signals when related tickets are saved or deleted
        and updates the order total.
        """

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)











