# events/api/views.py
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, parser_classes, renderer_classes
from rest_framework.response import Response
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.db.models import Q, Count, Max
from datetime import datetime, timedelta
from ..models import Event, Attendee, EventNote, EventsGroup
from .serializers import (
    EventSerializer, 
    AttendeeSerializer, 
    EventNoteSerializer,
    EventsGroupSerializer
)
from ..services.events_service import EventsService, EventsServiceError
from ..services.llm_config import LLMConfig
from .utils import error_response, success_response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..services.ollama_service import OllamaService
from rest_framework.renderers import JSONRenderer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from calendars.services.ics_service import ICSService
from rest_framework.decorators import renderer_classes,action
from calendars.renderers import ICSRenderer
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)

class EventsGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Events Groups.
    All operations are handled synchronously except for LLM API calls,
    which are managed within the EventsService.
    """
    serializer_class = EventsGroupSerializer
    queryset = EventsGroup.objects.all()
    events_service = EventsService()
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_queryset(self):
        """
        Get filtered and sorted queryset for events groups
        """
        queryset = EventsGroup.objects.all()
        
        # Apply filters if they exist
        queryset = self._apply_filters(
            queryset,
            self.request.query_params.get('search'),
            self.request.query_params.get('status'),
            self.request.query_params.get('event_type')
        )
        
        # Apply sorting
        return self._apply_sorting(
            queryset,
            self.request.query_params.get('sort', 'created_at'),
            self.request.query_params.get('order', 'desc')
        )

    def _apply_sorting(self, queryset, sort_field, sort_order):
        """Apply sorting to events group queryset."""
        valid_sort_fields = {
            'created_at': 'created_at',
            'event_count': Count('events'),  # Add annotation for event count
            'last_event': Max('events__start_datetime')  # Add annotation for latest event
        }

        if sort_field in valid_sort_fields:
            # Handle annotations for complex sorts
            if sort_field in ['event_count', 'last_event']:
                queryset = queryset.annotate(**{
                    sort_field: valid_sort_fields[sort_field]
                })
            
            # Apply sort direction
            sort_key = sort_field
            if sort_order == 'desc':
                sort_key = f"-{sort_field}"
            
            queryset = queryset.order_by(sort_key)
        else:
            # Default sort: newest first
            queryset = queryset.order_by('-created_at')

        return queryset

    def _apply_filters(self, queryset, search_term, status_filter, event_type):
        """Apply filters to events group queryset."""
        if search_term:
            queryset = queryset.filter(
                Q(events__title__icontains=search_term) |
                Q(events__location__icontains=search_term)
            ).distinct()

        if status_filter:
            status_mapping = {
                'completed': Q(processing_complete=True, processing_error=''),
                'processing': Q(processing_complete=False),
                'error': ~Q(processing_error='')
            }
            if status_filter in status_mapping:
                queryset = queryset.filter(status_mapping[status_filter])

        if event_type:
            queryset = queryset.filter(
                events__title__icontains=event_type.rstrip('s')  # Remove trailing 's'
            ).distinct()

        return queryset

    def retrieve(self, request, pk=None):
        """Get a single events group with all related data"""
        try:
            group = self.events_service.get_events_group(pk)
            
            # Get related events with attendees and notes
            events = group.events.all()
            
            return Response({
                'success': True,
                'data': {
                    'id': group.id,
                    'created_at': group.created_at,
                    'updated_at': group.updated_at,
                    'use_llm': group.use_llm,
                    'processing_complete': group.processing_complete,
                    'processing_error': group.processing_error,
                    'events': EventSerializer(events, many=True).data
                }
            })
            
        except EventsGroup.DoesNotExist:
            return Response({
                'success': False,
                'error': {
                    'message': f'Events group {pk} not found',
                    'code': 'GROUP_NOT_FOUND'
                }
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Error retrieving events group {pk}: {str(e)}")
            return Response({
                'success': False,
                'error': {
                    'message': 'Failed to retrieve events group',
                    'code': 'RETRIEVAL_ERROR'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'])
    def create_from_text(self, request):
        """Create event(s) from natural language text."""
        try:
            # Validate request data
            data = request.data
            text = data.get('text', '').strip()
            use_llm = data.get('use_llm', True)
            
            if not isinstance(use_llm, bool):
                use_llm = str(use_llm).lower() == 'true'
                
            if not text:
                return Response({
                    'success': False,
                    'error': {
                        'message': 'Text is required',
                        'code': 'MISSING_TEXT'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create event group and process text
            group = self.events_service.create_events_from_text(text, use_llm)
            first_event = group.events.first()
            multiple_events = group.events.count() > 1

            return Response({
                'success': True,
                'data': {
                    'group': EventsGroupSerializer(group).data,
                    'event': EventSerializer(first_event).data if first_event else None,
                    'multiple_events': multiple_events
                }
            }, status=status.HTTP_201_CREATED)

        except EventsServiceError as e:
            logger.error(f"Failed to create event from text: {str(e)}")
            return Response({
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 'EVENT_CREATION_ERROR'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Unexpected error in create_from_text: {str(e)}")
            return Response({
                'success': False,
                'error': {
                    'message': 'An unexpected error occurred',
                    'code': 'INTERNAL_ERROR'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    def destroy(self, request, *args, **kwargs):
        """
        Delete an events group and all its events.
        Handled synchronously via EventsService.
        """
        try:
            group_id = kwargs.get('pk')
            self.events_service.delete_events_group(group_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventsServiceError as e:
            logger.error(f"Failed to delete events group: {str(e)}")
            return Response({
                'success': False,
                'error': {'message': str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during deletion: {str(e)}")
            return Response({
                'success': False,
                'error': {'message': 'An unexpected error occurred'}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Get group processing status.
        Handled synchronously via EventsService.
        """
        try:
            group = self.events_service.get_events_group(pk)
            events = group.events.all()
            
            return success_response({
                'processing_complete': group.processing_complete,
                'processing_error': group.processing_error,
                'events': EventSerializer(events, many=True).data
            })
        except EventsServiceError as e:
            logger.error(f"Failed to retrieve group status: {str(e)}")
            return error_response(str(e), status_code=status.HTTP_400_BAD_REQUEST)

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing individual events.
    All operations are handled synchronously.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        """
        Get filtered and sorted queryset.
        Handled synchronously.
        """
        queryset = Event.objects.all()
        
        # Apply filters
        queryset = self._apply_filters(
            queryset,
            self.request.query_params.get('group'),
            self.request.query_params.get('search'),
            self.request.query_params.get('date_from'),
            self.request.query_params.get('date_to'),
            self.request.query_params.get('filter'),
            self.request.query_params.get('status')
        )
        
        # Apply sorting
        return self._apply_sorting(
            queryset,
            self.request.query_params.get('sort', 'start_datetime'),
            self.request.query_params.get('order', 'desc')
        )

    def _apply_filters(self, queryset, group_id, search_term, date_from, date_to, 
                       event_filter, status_filter):
        """Apply all filters to queryset synchronously."""
        
        # Filter by group if provided
        if group_id:
            queryset = queryset.filter(group_id=group_id)

        # Apply search if provided
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(location__icontains=search_term) |
                Q(venue__icontains=search_term) |
                Q(attendees__name__icontains=search_term)
            ).distinct()

        # Apply date filters
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                queryset = queryset.filter(start_datetime__date__gte=date_from)
            except ValueError:
                logger.warning(f"Invalid date_from format: {date_from}")

        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d')
                queryset = queryset.filter(start_datetime__date__lte=date_to)
            except ValueError:
                logger.warning(f"Invalid date_to format: {date_to}")

        # Apply event type filter
        if event_filter and event_filter != 'all':
            filter_mapping = {
                'meeting': 'meeting',
                'presentation': 'presentation',
                'review': 'review',
            }
            if event_filter in filter_mapping:
                queryset = queryset.filter(
                    title__icontains=filter_mapping[event_filter]
                )

        # Apply status filter
        if status_filter:
            status_mapping = {
                'complete': Q(processing_complete=True, processing_error__isnull=True),
                'pending': Q(processing_complete=False),
                'error': Q(processing_error__isnull=False) & ~Q(processing_error__exact='')
            }
            if status_filter in status_mapping:
                filter_condition = status_mapping[status_filter]
                queryset = queryset.filter(filter_condition)

        return queryset

    def _apply_sorting(self, queryset, sort_field, sort_order):
        """Apply sorting to queryset synchronously."""
        valid_sort_fields = {
            'start_datetime': 'start_datetime',
            'title': 'title',
            'created_at': 'created_at',
            'location': 'location',
            'status': 'processing_complete',
            'date': 'start_datetime__date'
        }

        if sort_field in valid_sort_fields:
            sort_key = valid_sort_fields[sort_field]
            if sort_order == 'desc':
                sort_key = f"-{sort_key}"
            queryset = queryset.order_by(sort_key)
        else:
            queryset = queryset.order_by('-start_datetime')

        return queryset

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Add note to event synchronously."""
        try:
            event = self.get_object()
            serializer = EventNoteSerializer(data=request.data)
            
            if serializer.is_valid():
                note = EventNote.objects.create(
                    event=event,
                    **serializer.validated_data
                )
                return success_response(
                    EventNoteSerializer(note).data, 
                    status=status.HTTP_201_CREATED
                )
            return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to add note: {str(e)}")
            return error_response('Failed to add note', status_code=500)

    @action(detail=True, methods=['post'])
    def add_attendee(self, request, pk=None):
        """Add attendee to event synchronously."""
        try:
            event = self.get_object()
            serializer = AttendeeSerializer(data=request.data)
            if serializer.is_valid():
                attendee = Attendee.objects.create(
                    event=event,
                    **serializer.validated_data
                )
                return success_response(
                    AttendeeSerializer(attendee).data, 
                    status=status.HTTP_201_CREATED
                )
            return error_response(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to add attendee: {str(e)}")
            return error_response('Failed to add attendee', status_code=500)
        
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Get event processing status
        """
        try:
            event = self.get_object()
            return success_response({
                'event': self.serializer_class(event).data,
                'processing_complete': event.processing_complete,
                'processing_error': event.processing_error
            })
        except Event.DoesNotExist:
            return error_response(
                'Event not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Failed to retrieve event status: {str(e)}")
            return error_response(
                'Failed to retrieve event status',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(
        detail=True,
        methods=['get'],
        url_path='download_ics',
        renderer_classes=[ICSRenderer, JSONRenderer]
    )
    def download_ics(self, request, pk=None):
        try:
            event = self.get_object()
            
            # Build description with both notes and suggestions
            description = []
            
            # Add notes if they exist
            if hasattr(event, 'notes') and event.notes.content:
                description.append("Notes:")
                description.append(event.notes.content)
                description.append("\n")
                
            # Add suggestions if they exist
            if event.suggestions:
                description.append("Suggestions:")
                # Handle both string and list formats of suggestions
                if isinstance(event.suggestions, str):
                    suggestions = event.suggestions.split('\n')
                else:
                    suggestions = event.suggestions
                    
                description.extend([f"- {suggestion.strip()}" for suggestion in suggestions])
                
            # Join all parts with newlines
            full_description = "\n".join(description)
            
            event_data = {
                'title': event.title,
                'start_datetime': event.start_datetime,
                'end_datetime': event.end_datetime,
                'description': full_description,
                'location': event.location,
                'attendees': [{'email': attendee.email} for attendee in event.attendees.all()],
            }
            
            ics_content = ICSService.create_ics_event(event_data)
            
            response = HttpResponse(ics_content, content_type='text/calendar')
            response['Content-Disposition'] = f'attachment; filename="{event.title}.ics"'
            return response
            
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error creating ICS file: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def llm_config_view(request):
    """Return LLM configuration settings synchronously."""
    try:
        config = LLMConfig()
        return success_response({
            'provider': config.provider,
            'config': config.config
        })
    except Exception as e:
        logger.error(f"Failed to retrieve LLM config: {str(e)}")
        return error_response('Failed to retrieve LLM config', status_code=500)

@api_view(['GET'])
def global_search(request):
    """
    Global search endpoint for events and attendees.
    Handled synchronously.
    """
    try:
        query = request.query_params.get('q', '')
        if not query or len(query) < 2:  # Minimum 2 characters for search
            return success_response([])

        # Regular synchronous queries
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(venue__icontains=query)
        ).values(
            'id', 
            'title', 
            'location', 
            'original_text', 
            'notes__content'
        )[:5]
        
        attendees = Attendee.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        ).select_related('event').values(
            'id',
            'name',
            'email',
            'event__id',
            'event__title'
        )[:5]
        
        results = []
        
        # Format event results
        for event in events:
            snippet = (
                event.get('notes__content', '')[:100] if event.get('notes__content')
                else event.get('original_text', '')[:100] if event.get('original_text')
                else ''
            )
            results.append({
                'id': f'event_{event["id"]}',
                'type': 'event',
                'title': event['title'],
                'url': f'/events/{event["id"]}',
                'snippet': snippet
            })
        
        # Format attendee results
        for attendee in attendees:
            results.append({
                'id': f'attendee_{attendee["id"]}',
                'type': 'attendee',
                'title': attendee['name'],
                'url': f'/events/{attendee["event__id"]}',
                'snippet': f'Attendee of {attendee["event__title"]}'
            })
        
        return success_response(results)
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return error_response(
            'Failed to perform search',
            status_code=500
        )

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def check_ollama_status(request):
    """Check Ollama server connectivity"""
    try:
        base_url = request.GET.get('base_url', 'http://localhost:11434')
        ollama_service = OllamaService(base_url=base_url)
        
        # Use sync_to_async to call the async method
        is_connected = async_to_sync(ollama_service.check_connectivity)()
        
        return success_response({
            'is_connected': is_connected
        })
        
    except Exception as e:
        logger.error(f"Failed to check Ollama status: {str(e)}")
        return error_response(
            str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_ollama_models(request):
    """Get available Ollama models"""
    try:
        base_url = request.GET.get('base_url', 'http://localhost:11434')
        ollama_service = OllamaService(base_url=base_url)
        
        # Use sync_to_async to call the async method
        models = async_to_sync(ollama_service.get_available_models)()
        
        return success_response({
            'models': models
        })
    except Exception as e:
        logger.error(f"Failed to get Ollama models: {str(e)}")
        return error_response(
            str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )