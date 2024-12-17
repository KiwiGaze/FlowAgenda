# calendars/models.py
from django.db import models
from events.models import Event
import uuid

class CalendarProvider(models.Model):
    PROVIDER_CHOICES = [
        ('google', 'Google Calendar'),
        ('outlook', 'Outlook Calendar'),
        ('apple', 'Apple Calendar'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    is_connected = models.BooleanField(default=False)
    last_synced = models.DateTimeField(null=True, blank=True)
    credentials = models.JSONField(default=dict, blank=True) # Store OAuth tokens here
    settings = models.JSONField(default=dict, blank=True) # Store provider-specific settings here
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.get_name_display()} - {'Connected' if self.is_connected else 'Disconnected'}"
    
class EventSync(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='syncs')
    provider = models.ForeignKey(CalendarProvider, on_delete=models.CASCADE)
    provider_event_id = models.CharField(max_length=255) # Store provider's event ID here
    last_synced = models.DateTimeField(auto_now=True)
    sync_status = models.CharField(max_length=50, default='pending') # success, error, warning, info

    class Meta:
        unique_together = ['event', 'provider']
        ordering = ['-last_synced']

    def __str__(self):
        return f"{self.event.title} - {self.provider.name} sync"

class UserPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=50, unique=True)
    value = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key