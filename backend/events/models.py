# events/models.py
from django.db import models
import uuid
from typing import List, Dict, Optional

class EventsGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    use_llm = models.BooleanField(default=False) # Use LLM API for processing.  
    processing_complete = models.BooleanField(default=False)    
    processing_error = models.TextField(blank=True)

    def __str__(self):
        return f"Events Group {self.id} - {self.created_at}"
    
    class Meta:
        ordering = ['created_at']
    
    async def get_events(self) -> List['Event']:
        """Get all events for this group"""
        return  await self.events.all()
    
    async def get_num_events(self) -> int:
        """Get number of events in this group"""
        return await self.events.count()
    
    @staticmethod
    async def get_or_create_default_group() -> Optional['EventsGroup']:
        """Get or create default events group"""
        try:
            # Try to get the first group
            default_group = await EventsGroup.objects.afirst()
            if not default_group:
                default_group = await EventsGroup.objects.acreate()
            return default_group
        except Exception:
            return None

class Event(models.Model):
    group = models.ForeignKey(
        EventsGroup, 
        related_name='events', 
        on_delete=models.CASCADE,
        null=True,  # Temporarily allow null
        blank=True
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)  # Suggestions for the event.

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    original_text = models.TextField(blank=True) # Store original natural language text.
    processing_complete = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)

    class Meta:
        ordering = ['start_datetime']
    
    def __str__(self):
        return f"{self.title} on {self.start_datetime.date()} at {self.start_datetime.time()}"
    
    async def get_attendees(self) -> List['Attendee']:
        """Get all attendees for this event"""
        return await self.attendees.all()

    async def get_notes(self) -> List['EventNote']:
        """Get all notes for this event"""
        return await self.notes.all()

class Attendee(models.Model):
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class EventNote(models.Model):
    event = models.OneToOneField(Event, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.event.title} - {self.created_at}"
