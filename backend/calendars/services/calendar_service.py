# calendars/services/calendar_service.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from django.conf import settings
import aiohttp
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class CalendarServiceError(Exception):
    """Custom exception for calendar service errors"""
    pass

class BaseCalendarService(ABC):
    """Abstract base class for calendar service providers"""
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Authenticate with the calendar service"""
        pass
        
    @abstractmethod
    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an event in the calendar"""
        pass
        
    @abstractmethod
    async def get_calendars(self) -> List[Dict[str, Any]]:
        """Get list of available calendars"""
        pass

class GoogleCalendarService(BaseCalendarService):
    """Google Calendar implementation"""
    
    def __init__(self):
        self.client_id = settings.CALENDAR_PROVIDER['google']['client_id']
        self.base_url = "https://www.googleapis.com/calendar/v3"
        self.token = None
        
    async def authenticate(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Authenticate with Google Calendar"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://oauth2.googleapis.com/token",
                    json={
                        "client_id": self.client_id,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "code": credentials["code"],
                        "grant_type": "authorization_code",
                        "redirect_uri": credentials["redirect_uri"]
                    }
                ) as response:
                    if response.status != 200:
                        raise CalendarServiceError("Failed to authenticate with Google")
                    
                    data = await response.json()
                    self.token = data["access_token"]
                    return data
                    
        except Exception as e:
            logger.error(f"Google Calendar authentication failed: {str(e)}")
            raise CalendarServiceError(f"Authentication failed: {str(e)}")
    
    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create event in Google Calendar"""
        if not self.token:
            raise CalendarServiceError("Not authenticated")
            
        try:
            # Format event data for Google Calendar
            formatted_event = {
                "summary": event_data["title"],
                "description": event_data.get("notes", ""),
                "start": {
                    "dateTime": event_data["start_datetime"].isoformat(),
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": event_data["end_datetime"].isoformat(),
                    "timeZone": "UTC"
                },
                "location": event_data.get("location", ""),
                "attendees": [
                    {"email": attendee["email"]}
                    for attendee in event_data.get("attendees", [])
                    if attendee.get("email")
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/calendars/primary/events",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=formatted_event
                ) as response:
                    if response.status != 200:
                        raise CalendarServiceError("Failed to create event")
                        
                    return await response.json()
                    
        except Exception as e:
            logger.error(f"Failed to create Google Calendar event: {str(e)}")
            raise CalendarServiceError(f"Event creation failed: {str(e)}")
    
    async def get_calendars(self) -> List[Dict[str, Any]]:
        """Get available Google Calendars"""
        if not self.token:
            raise CalendarServiceError("Not authenticated")
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/users/me/calendarList",
                    headers={"Authorization": f"Bearer {self.token}"}
                ) as response:
                    if response.status != 200:
                        raise CalendarServiceError("Failed to fetch calendars")
                        
                    data = await response.json()
                    return data.get("items", [])
                    
        except Exception as e:
            logger.error(f"Failed to fetch Google Calendars: {str(e)}")
            raise CalendarServiceError(f"Calendar fetch failed: {str(e)}")

class OutlookCalendarService(BaseCalendarService):
    """Outlook Calendar implementation"""
    
    def __init__(self):
        self.client_id = settings.CALENDAR_PROVIDER['outlook']['client_id']
        self.base_url = "https://graph.microsoft.com/v1.0/me"
        self.token = None
        
    async def authenticate(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Authenticate with Outlook Calendar"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                    data={
                        "client_id": self.client_id,
                        "client_secret": settings.OUTLOOK_CLIENT_SECRET,
                        "code": credentials["code"],
                        "grant_type": "authorization_code",
                        "redirect_uri": credentials["redirect_uri"],
                        "scope": "Calendars.ReadWrite"
                    }
                ) as response:
                    if response.status != 200:
                        raise CalendarServiceError("Failed to authenticate with Outlook")
                    
                    data = await response.json()
                    self.token = data["access_token"]
                    return data
                    
        except Exception as e:
            logger.error(f"Outlook Calendar authentication failed: {str(e)}")
            raise CalendarServiceError(f"Authentication failed: {str(e)}")
    
    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create event in Outlook Calendar"""
        if not self.token:
            raise CalendarServiceError("Not authenticated")
            
        try:
            # Format event data for Outlook Calendar
            formatted_event = {
                "subject": event_data["title"],
                "body": {
                    "contentType": "text",
                    "content": event_data.get("notes", "")
                },
                "start": {
                    "dateTime": event_data["start_datetime"].isoformat(),
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": event_data["end_datetime"].isoformat(),
                    "timeZone": "UTC"
                },
                "location": {
                    "displayName": event_data.get("location", "")
                },
                "attendees": [
                    {
                        "emailAddress": {"address": attendee["email"]},
                        "type": "required"
                    }
                    for attendee in event_data.get("attendees", [])
                    if attendee.get("email")
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/events",
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json"
                    },
                    json=formatted_event
                ) as response:
                    if response.status != 201:
                        raise CalendarServiceError("Failed to create event")
                        
                    return await response.json()
                    
        except Exception as e:
            logger.error(f"Failed to create Outlook Calendar event: {str(e)}")
            raise CalendarServiceError(f"Event creation failed: {str(e)}")
    
    async def get_calendars(self) -> List[Dict[str, Any]]:
        """Get available Outlook Calendars"""
        if not self.token:
            raise CalendarServiceError("Not authenticated")
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/calendars",
                    headers={"Authorization": f"Bearer {self.token}"}
                ) as response:
                    if response.status != 200:
                        raise CalendarServiceError("Failed to fetch calendars")
                        
                    data = await response.json()
                    return data.get("value", [])
                    
        except Exception as e:
            logger.error(f"Failed to fetch Outlook Calendars: {str(e)}")
            raise CalendarServiceError(f"Calendar fetch failed: {str(e)}")

class CalendarServiceFactory:
    """Factory for creating calendar service instances"""
    
    @staticmethod
    def create_service(provider: str) -> BaseCalendarService:
        """Create appropriate calendar service instance"""
        if provider == "google":
            return GoogleCalendarService()
        elif provider == "outlook":
            return OutlookCalendarService()
        else:
            raise ValueError(f"Unsupported calendar provider: {provider}")