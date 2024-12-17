# events/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Count
from .models import Event, EventsGroup

@receiver(post_delete, sender=Event)
def delete_empty_group(sender, instance, **kwargs):
    """
    Signal handler to delete EventsGroup when its last event is deleted
    
    This function is called after an Event is deleted. It checks if the
    associated EventsGroup has any remaining events, and if not, deletes
    the group.
    """
    if instance.group:
        # Check if the group exists and has no remaining events
        try:
            group = EventsGroup.objects.annotate(
                event_count=Count('events')
            ).get(id=instance.group.id)
            
            if group.event_count == 0:
                group.delete()
                
        except EventsGroup.DoesNotExist:
            # Group was already deleted
            pass