# events/services/events_service.py
from typing import Dict, List, Any, Optional
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from ..models import Event, EventsGroup, Attendee, EventNote
from .llm_service import LLMService, LLMServiceError
from .ollama_service import OllamaService
import logging
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

class EventsServiceError(Exception):
    """Custom exception for events service errors"""
    pass

class EventsService:
    """Service for managing events and event groups"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.ollama_service = OllamaService(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL
        )

    @transaction.atomic
    def create_events_from_text(self, text: str, use_llm: bool = True) -> EventsGroup:
        """
        Create multiple events from natural language text using either cloud LLM or local Ollama
        
        Args:
            text: Natural language text to parse
            use_llm: If True, use cloud LLM, if False use local Ollama
            
        Returns:
            EventsGroup: Created events group
            
        Raises:
            EventsServiceError: If event creation fails
        """
        try:
            # Input validation
            if not text or not text.strip():
                raise EventsServiceError("Text input cannot be empty")

            # Create event group
            group = EventsGroup.objects.create(
                use_llm=use_llm,
                processing_complete=False
            )
            
            try:
                # Choose service based on use_llm flag
                if use_llm:
                    logger.info(f"Processing text with cloud LLM for group {group.id}")
                    service = self.llm_service
                else:
                    logger.info(f"Processing text with local Ollama for group {group.id}")
                    service = self.ollama_service
                
                # Parse events using selected service
                parsed_events = async_to_sync(service.parse_events)(text, group)
                
                if not parsed_events:
                    raise EventsServiceError("No events were parsed from the text")
                
                # Store original text and process events
                for event_data in parsed_events:
                    event_data['original_text'] = text
                
                # Create events from parsed data
                created_events = self._create_events_from_parsed_data(parsed_events, group)
                
                # Update group status
                group.processing_complete = True
                group.save()
                
                logger.info(f"Successfully created {len(created_events)} events for group {group.id}")
                
                return group
                
            except (LLMServiceError) as e:
                error_msg = f"{'LLM' if use_llm else 'Ollama'} processing failed: {str(e)}"
                self._handle_processing_error(group, error_msg)
                raise EventsServiceError(error_msg)
                
            except Exception as e:
                error_msg = f"Unexpected error during event processing: {str(e)}"
                self._handle_processing_error(group, error_msg)
                raise EventsServiceError(error_msg)

        except Exception as e:
            logger.error(f"Failed to create events from text: {str(e)}")
            raise EventsServiceError(f"Event creation failed: {str(e)}")

    def _handle_processing_error(self, group: EventsGroup, error_msg: str):
        """Handle processing errors by updating group status"""
        logger.error(f"{error_msg} for group {group.id}")
        group.processing_error = error_msg
        group.processing_complete = True
        group.save()

    def _create_events_from_parsed_data(
        self, 
        parsed_events: List[Dict[str, Any]], 
        group: EventsGroup
    ) -> List[Event]:
        """
        Create events and related objects from parsed data
        
        Args:
            parsed_events: List of parsed event data dictionaries
            group: Parent EventsGroup
            
        Returns:
            List of created Event objects
            
        Raises:
            EventsServiceError: If event creation fails
        """
        try:
            created_events = []
            for event_data in parsed_events:
                try:
                    event = self._create_single_event(event_data, group)
                    created_events.append(event)
                except Exception as e:
                    logger.error(
                        f"Failed to create event in group {group.id}: {str(e)}\n"
                        f"Event data: {event_data}"
                    )
                    raise
            return created_events
            
        except Exception as e:
            logger.error(f"Failed to create events from parsed data: {str(e)}")
            raise EventsServiceError(f"Failed to create events: {str(e)}")

    @transaction.atomic
    def _create_single_event(
        self, 
        event_data: Dict[str, Any], 
        group: EventsGroup
    ) -> Event:
        """
        Create a single event and its related objects
        
        Args:
            event_data: Dictionary containing event data
            group: Parent EventsGroup
            
        Returns:
            Created Event object
        """
        try:
            # Validate required fields
            required_fields = ['title', 'start_datetime']
            for field in required_fields:
                if field not in event_data:
                    raise EventsServiceError(f"Missing required field: {field}")

            # Create the event with default values for optional fields
            event = Event.objects.create(
                group=group,
                title=event_data['title'],
                start_datetime=event_data['start_datetime'],
                end_datetime=event_data.get('end_datetime'),
                location=event_data.get('location', ''),
                venue=event_data.get('venue', ''),
                suggestions=event_data.get('suggestions', ''),
                original_text=event_data.get('original_text', ''),
                processing_complete=True
            )

            # Create initial note if provided
            if notes := event_data.get('notes'):
                self._create_event_note(event, notes)

            # Create attendees if present
            if attendees := event_data.get('attendees'):
                self._create_attendees(event, attendees)

            return event

        except Exception as e:
            logger.error(f"Failed to create single event: {str(e)}")
            raise EventsServiceError(f"Failed to create event: {str(e)}")

    def _create_event_note(
        self, 
        event: Event, 
        note_content: str
    ) -> Optional[EventNote]:
        """Create a note for an event"""
        try:
            if not note_content:
                return None
                
            return EventNote.objects.create(
                event=event,
                content=note_content
            )
        except Exception as e:
            logger.error(f"Failed to create event note: {str(e)}")
            raise EventsServiceError(f"Failed to create event note: {str(e)}")

    def _create_attendees(
        self, 
        event: Event, 
        attendees_data: List[Dict[str, str]]
    ) -> List[Attendee]:
        """Create attendees for an event"""
        try:
            created_attendees = []
            for attendee_data in attendees_data:
                if not attendee_data.get('name'):
                    continue
                    
                attendee = Attendee.objects.create(
                    event=event,
                    name=attendee_data['name'],
                    email=attendee_data.get('email', '')
                )
                created_attendees.append(attendee)
            return created_attendees
            
        except Exception as e:
            logger.error(f"Failed to create attendees: {str(e)}")
            raise EventsServiceError(f"Failed to create attendees: {str(e)}")

    def get_events_group(self, group_id: str) -> EventsGroup:
        """
        Get events group with all related events
        
        Args:
            group_id: UUID of the events group
            
        Returns:
            EventsGroup with related data
            
        Raises:
            EventsServiceError: If group not found or retrieval fails
        """
        try:
            group = EventsGroup.objects.prefetch_related(
                'events__attendees',
                'events__notes'
            ).get(id=group_id)
            
            return group
            
        except EventsGroup.DoesNotExist:
            raise EventsServiceError(f"Events group {group_id} not found")
        except Exception as e:
            logger.error(f"Error retrieving events group {group_id}: {str(e)}")
            raise EventsServiceError(f"Failed to retrieve events group: {str(e)}")

    @transaction.atomic
    def delete_events_group(self, group_id: str) -> None:
        """
        Delete an events group and all related events
        
        Args:
            group_id: UUID of the events group to delete
            
        Raises:
            EventsServiceError: If deletion fails
        """
        try:
            group = EventsGroup.objects.select_related(
                'events'
            ).get(id=group_id)
            
            # Log deletion
            logger.info(f"Deleting events group {group_id} with {group.events.count()} events")
            
            group.delete()
            logger.info(f"Successfully deleted events group {group_id}")
            
        except EventsGroup.DoesNotExist:
            raise EventsServiceError(f"Events group {group_id} not found")
        except Exception as e:
            logger.error(f"Failed to delete events group {group_id}: {str(e)}")
            raise EventsServiceError(f"Failed to delete events group: {str(e)}")
        
    async def check_ollama_connectivity(self) -> bool:
        """Check connectivity to Ollama service"""
        try:
            return await self.ollama_service.check_connectivity()
        except Exception as e:
            logger.error(f"Failed to check Ollama connectivity: {str(e)}")
            return False
    
    
