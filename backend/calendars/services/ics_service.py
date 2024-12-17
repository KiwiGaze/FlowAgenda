# calendars/services/ics_service.py
from datetime import datetime
from typing import Dict, Any
import uuid
from icalendar import Calendar, Event as ICSEvent
from django.http import HttpResponse

class ICSService:
    """Service for handling ICS file operations"""
    
    @staticmethod
    def create_ics_event(event_data: Dict[str, Any]) -> str:
        """
        Create an ICS file content from event data
        
        Args:
            event_data: Dictionary containing event details
                Required keys: title, start_datetime, end_datetime
                Optional keys: description, location, attendees
                
        Returns:
            String containing ICS file content
        """
        # Create calendar
        cal = Calendar()
        cal.add('prodid', '-//My Calendar Application//example.com//')
        cal.add('version', '2.0')
        
        # Create event
        event = ICSEvent()
        event.add('summary', event_data['title'])
        event.add('dtstart', event_data['start_datetime'])
        event.add('dtend', event_data['end_datetime'])
        
        # Add optional fields if they exist
        if event_data.get('description'):
            event.add('description', event_data['description'])
        
        if event_data.get('location'):
            event.add('location', event_data['location'])
            
        # Add unique identifier
        event.add('uid', str(uuid.uuid4()))
        
        # Add creation timestamp
        event.add('dtstamp', datetime.utcnow())
        
        # Add attendees if they exist
        for attendee in event_data.get('attendees', []):
            if attendee.get('email'):
                event.add('attendee', f'mailto:{attendee["email"]}')
        
        # Add event to calendar
        cal.add_component(event)
        
        return cal.to_ical()

    @staticmethod
    def create_response(ics_content: bytes, filename: str = None) -> HttpResponse:
        """
        Create HTTP response with ICS file
        
        Args:
            ics_content: Byte string of ICS file content
            filename: Optional filename (default: event.ics)
            
        Returns:
            HttpResponse object with ICS file
        """
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="{filename or "event.ics"}"'
        return response