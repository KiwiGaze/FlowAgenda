# tests/test_llm_service.py
from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from freezegun import freeze_time  # Add this import
from ..services.llm_service import LLMService, LLMServiceError
import json

class TestLLMService(TestCase):
    def setUp(self):
        self.service = LLMService()
        self.sample_text = "Schedule a project review meeting with Sarah and Mike in Room 204 next Tuesday at 2:30 PM to discuss Q1 results"
        
    def test_datetime_awareness(self):
        """Test datetime objects for timezone awareness"""
        now = datetime.now()
        tz_now = timezone.now()
        
        self.assertIsNone(now.tzinfo, "datetime.now() should be naive")
        self.assertIsNotNone(tz_now.tzinfo, "timezone.now() should be aware")

    @patch('openai.OpenAI')
    def test_validate_dates_timezone_handling(self, mock_openai):
        """Test date validation with timezone-aware and naive datetimes"""
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        
        test_data = {
            'title': 'Test Meeting',
            'start_date': tomorrow.strftime('%Y-%m-%d'),
            'start_time': '14:00',
        }
        
        try:
            self.service._validate_dates(test_data)
        except LLMServiceError as e:
            self.fail(f"Validation failed with error: {str(e)}")

    @freeze_time("2024-11-09")  # Freeze time to a Saturday
    @patch('openai.OpenAI')
    def test_parse_event_full_flow(self, mock_openai):
        """Test complete event parsing flow with mock LLM response"""
        # Next Tuesday will be 2024-11-12
        next_tuesday = timezone.now().date() + timedelta(days=3)
        print(timezone.now().date())
        
        # Create mock LLM response that matches expected format
        mock_llm_response = {
            'title': 'Project Review Meeting',
            'start_date': next_tuesday.strftime('%Y-%m-%d'),
            'start_time': '14:30',
            'description': 'Q1 results discussion',
            'location': 'Room 204',  # Changed from venue to location
            'attendees': ['Sarah', 'Mike']
        }
        
        # Setup mock completion
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content=json.dumps(mock_llm_response)))
        ]
        mock_openai.return_value.chat.completions.create.return_value = mock_completion
        
        try:
            result = self.service.parse_event(self.sample_text)
            
            # Print debug info
            print(f"Result received: {result}")
            
            # Verify expected fields
            self.assertEqual(result['start_date'], next_tuesday.strftime('%Y-%m-%d'))
            self.assertEqual(result['start_time'], '14:30')
            
        except Exception as e:
            self.fail(f"Event parsing failed: {str(e)}")

    def test_date_comparison_edge_cases(self):
        """Test specific date comparison scenarios"""
        today = timezone.now().date()
        
        # Test past date
        past_data = {
            'start_date': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
            'start_time': '14:00'
        }
        
        with self.assertRaises(LLMServiceError):
            self.service._validate_dates(past_data)
        
        # Test same-day time ordering
        same_day_data = {
            'start_date': today.strftime('%Y-%m-%d'),
            'start_time': '14:00',
            'end_date': today.strftime('%Y-%m-%d'),
            'end_time': '13:00'
        }
        
        with self.assertRaises(LLMServiceError):
            self.service._validate_dates(same_day_data)