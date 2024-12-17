import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, AsyncMock
from ..models import EventsGroup, Event
from ..services.events_service import EventsServiceError
from .utils import error_response, success_response

# backend/events/api/test_views.py

pytestmark = pytest.mark.django_db

class TestEventsGroupViewSet:
    @pytest.fixture
    def api_client(self, client):
        return client
        
    @pytest.fixture
    def create_from_text_url(self):
        return reverse('eventsgroup-create-from-text')

    async def test_create_from_text_success(self, api_client, create_from_text_url):
        """Test successful event creation from text"""
        # Mock data
        sample_text = "Meeting with team tomorrow at 3pm"
        mock_group = EventsGroup(id=1, processing_complete=True)
        mock_event = Event(id=1, title="Team Meeting")
        
        # Mock service call
        with patch('events.services.events_service.EventsService.create_events_from_text', 
                  new_callable=AsyncMock) as mock_service:
            mock_service.return_value = mock_group
            
            # Mock relationship methods
            mock_group.events = AsyncMock()
            mock_group.events.afirst.return_value = mock_event
            mock_group.events.acount.return_value = 1

            response = await api_client.post(
                create_from_text_url,
                {"text": sample_text, "use_llm": True},
                content_type="application/json"
            )

            assert response.status_code == status.HTTP_201_CREATED
            assert response.json() == {
                "success": True,
                "data": {
                    "group": {"id": 1, "processing_complete": True},
                    "event": {"id": 1, "title": "Team Meeting"},
                    "multiple_events": False
                }
            }

    async def test_create_from_text_missing_text(self, api_client, create_from_text_url):
        """Test error handling for missing text"""
        response = await api_client.post(
            create_from_text_url,
            {},
            content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "success": False,
            "error": {
                "message": "Text is required",
                "status_code": status.HTTP_400_BAD_REQUEST
            }
        }

    async def test_create_from_text_service_error(self, api_client, create_from_text_url):
        """Test error handling for service errors"""
        with patch('events.services.events_service.EventsService.create_events_from_text',
                  new_callable=AsyncMock) as mock_service:
            mock_service.side_effect = EventsServiceError("Failed to process text")

            response = await api_client.post(
                create_from_text_url,
                {"text": "Invalid text"},
                content_type="application/json"
            )

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {
                "success": False,
                "error": {
                    "message": "Failed to process text",
                    "status_code": status.HTTP_400_BAD_REQUEST
                }
            }

    async def test_create_from_text_without_llm(self, api_client, create_from_text_url):
        """Test event creation without LLM"""
        sample_text = "Meeting tomorrow"
        mock_group = EventsGroup(id=1, processing_complete=True)
        mock_event = Event(id=1, title="Meeting")

        with patch('events.services.events_service.EventsService.create_events_from_text',
                  new_callable=AsyncMock) as mock_service:
            mock_service.return_value = mock_group
            mock_group.events = AsyncMock()
            mock_group.events.afirst.return_value = mock_event
            mock_group.events.acount.return_value = 1

            response = await api_client.post(
                create_from_text_url,
                {"text": sample_text, "use_llm": False},
                content_type="application/json"
            )

            assert response.status_code == status.HTTP_201_CREATED
            mock_service.assert_called_with(sample_text, False)

    async def test_create_from_text_multiple_events(self, api_client, create_from_text_url):
        """Test creation of multiple events"""
        sample_text = "Weekly meetings every Monday at 10am"
        mock_group = EventsGroup(id=1, processing_complete=True)
        mock_event = Event(id=1, title="Weekly Meeting")

        with patch('events.services.events_service.EventsService.create_events_from_text',
                  new_callable=AsyncMock) as mock_service:
            mock_service.return_value = mock_group
            mock_group.events = AsyncMock()
            mock_group.events.afirst.return_value = mock_event
            mock_group.events.acount.return_value = 4

            response = await api_client.post(
                create_from_text_url,
                {"text": sample_text, "use_llm": True},
                content_type="application/json"
            )

            assert response.status_code == status.HTTP_201_CREATED
            response_data = response.json()
            assert response_data["data"]["multiple_events"] is True