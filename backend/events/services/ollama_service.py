# events/services/ollama_service.py
import aiohttp
import json
from typing import Dict, Any, List
from datetime import datetime
import logging
from .llm_service import LLMServiceError
from datetime import timedelta

logger = logging.getLogger(__name__)

class OllamaService:
    """Service for processing natural language using Ollama local LLM"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2"):
        self.base_url = base_url
        self.model = model

    async def check_connectivity(self) -> bool:
        """Check if the service can connect to the Ollama server"""
        try:
            async with aiohttp.ClientSession() as session:
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=timeout
                ) as response:
                    return response.status == 200
        except aiohttp.ClientError as e:
            logger.error(f"Ollama connectivity check failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during Ollama connectivity check: {str(e)}")
            return False

    async def get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status != 200:
                        return []
                    data = await response.json()
                    return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            logger.error(f"Failed to get available models: {str(e)}")
            return []
        
    def set_model(self, model_name: str):
        """Set the model to use for generation"""
        self.model = model_name

    def _format_events_data(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format the events data to match the expected structure"""
        formatted_events = []
        
        for event in events:
            try:
                # Validate required fields
                required_fields = ['title', 'start_date', 'start_time']
                for field in required_fields:
                    if field not in event:
                        raise LLMServiceError(f"Missing required field: {field}")

                # Create datetime objects
                start_datetime = datetime.strptime(
                    f"{event['start_date']} {event['start_time']}", 
                    '%Y-%m-%d %H:%M'
                )
                
                # Handle end datetime
                if event.get('end_date') and event.get('end_time'):
                    end_datetime = datetime.strptime(
                        f"{event['end_date']} {event['end_time']}", 
                        '%Y-%m-%d %H:%M'
                    )
                elif event.get('end_time'):
                    # If only end_time is provided, use start_date
                    end_time = datetime.strptime(event['end_time'], '%H:%M').time()
                    end_datetime = datetime.combine(start_datetime.date(), end_time)
                else:
                    # Default to 1 hour duration
                    end_datetime = start_datetime + timedelta(hours=1)

                # Format attendees data
                attendees = []
                if 'attendees' in event:
                    for attendee in event['attendees']:
                        if isinstance(attendee, dict):
                            attendees.append({
                                'name': attendee.get('name', ''),
                                'email': attendee.get('email', '')
                            })
                        else:
                            # Handle string-only attendees
                            attendees.append({'name': str(attendee), 'email': ''})
                
                # Ensure suggestions is a list and join with newlines
                suggestions = event.get('suggestions', [])
                if not isinstance(suggestions, list):
                    suggestions = []
                if not suggestions:
                    suggestions = ["Remember to confirm attendance", "Set up a reminder"]

                # Format the event data
                formatted_event = {
                    'title': event['title'],
                    'start_datetime': start_datetime,
                    'end_datetime': end_datetime,
                    'location': event.get('location', ''),
                    'venue': event.get('venue', ''),
                    'notes': event.get('notes', ''),
                    'suggestions': '\n'.join(suggestions),
                    'attendees': attendees
                }
                
                formatted_events.append(formatted_event)
                
            except (ValueError, KeyError) as e:
                raise LLMServiceError(f"Error formatting event data: {str(e)}")
                
        return formatted_events

    def _format_prompt(self, text: str) -> str:
        """Format the input text into a detailed prompt supporting multiple event parsing"""
        today = datetime.now()
        weekday = today.strftime('%A')
        
        return f"""Please parse the following text into one or more events and return the result as JSON.

    Today is {today.strftime('%Y-%m-%d')} ({weekday}). 

    The text may contain multiple events. Please analyze and identify if multiple events are described.

    Return your response as a JSON object with the following structure:
    {{
        "is_multi_event": boolean,  # True if multiple events detected
        "events": [  # Array of events (even for single event)
            {{
                "title": string (required),
                "start_date": "YYYY-MM-DD" (required),
                "start_time": "HH:MM" 24-hour format (required),
                "end_date": "YYYY-MM-DD" (if not provided, use start_date),
                "end_time": "HH:MM" 24-hour format (if not provided, start_time + 1 hour),
                "location": string (optional),
                "venue": string (optional),
                "attendees": [
                    {{
                        "name": string,
                        "email": string (optional)
                    }}
                ],
                "notes": string (optional - special instructions/reminders),
                "suggestions": array of strings (1-2 helpful suggestions) (required)
            }}
        ]
    }}

    Text to parse: {text}

    Remember to return only valid JSON matching the above structure without any additional text or explanations."""

    async def parse_events(self, text: str, group) -> List[Dict[str, Any]]:
        """
        Parse natural language text into structured event data using Ollama
        
        Args:
            text: The natural language text to parse
            group: The EventsGroup (kept for compatibility with LLMService)
        
        Returns:
            List of parsed event dictionaries
        """
        try:
            prompt = self._format_prompt(text)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                ) as response:
                    if response.status != 200:
                        raise LLMServiceError(f"Ollama API returned status {response.status}")
                    
                    result = await response.json()
                    response_text = result.get('response', '')
                    
                    # Clean up response text to ensure valid JSON
                    json_str = response_text.strip()
                    if json_str.startswith('```json'):
                        json_str = json_str.split('```json')[1].split('```')[0]
                    
                    try:
                        parsed_data = json.loads(json_str)
                    except json.JSONDecodeError as e:
                        raise LLMServiceError(f"Failed to parse Ollama response as JSON: {str(e)}")
                    
                    # Validate response structure
                    if not isinstance(parsed_data, dict) or 'events' not in parsed_data:
                        raise LLMServiceError("Invalid response format from Ollama")
                    
                    if not isinstance(parsed_data['events'], list):
                        raise LLMServiceError("Events must be an array")
                    
                    # Format events data
                    return self._format_events_data(parsed_data['events'])
                        
        except aiohttp.ClientError as e:
            raise LLMServiceError(f"Failed to connect to Ollama service: {str(e)}")
        except Exception as e:
            raise LLMServiceError(f"Ollama processing failed: {str(e)}")