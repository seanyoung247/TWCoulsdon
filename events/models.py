from django.db import models
from datetime import datetime 


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
        
    
class Event(models.Model):
    pass