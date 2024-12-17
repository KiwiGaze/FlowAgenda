# events/api/serializers.py
from rest_framework import serializers
from events.models import Event, Attendee, EventNote, EventsGroup
from datetime import datetime, timedelta

class AttendeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email']

    def validate_email(self, value):
        """
        Custom validation for email field
        """
        if value is None or value.strip() == '':
            return None
        return value.strip()

class EventNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNote
        fields = ['id', 'content', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    attendees = AttendeeSerializer(many=True, required=False)
    notes = EventNoteSerializer(many=False, required=False, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'group', 'title', 'start_datetime', 'end_datetime',
            'location', 'venue', 'attendees', 'notes', 'created_at', 'updated_at', 
            'original_text', 'processing_complete', 'processing_error',
            'suggestions'
        ]

    def validate(self, data):
        """
        Validate the event data.
        """
        if data.get('title') == 'Processing...':
            return data

        # Initialize optional fields with empty strings if not provided
        for field in ['location', 'venue']:
            if field not in data:
                data[field] = ''

        if 'start_datetime' in data:
            if data['start_datetime'].replace(tzinfo=None) < datetime.now():
                raise serializers.ValidationError("Schedule cannot be in the past.")
        
        if 'end_datetime' in data and data.get('start_datetime'):
            if data['end_datetime'].replace(tzinfo=None) < data['start_datetime'].replace(tzinfo=None):
                raise serializers.ValidationError("End time cannot be before start time.")
            
        return data

    def create(self, validated_data):
        """Synchronous create method."""
        # Handle end_datetime default logic
        if 'end_datetime' not in validated_data and 'start_datetime' in validated_data:
            if validated_data.get('title') != 'Processing...':
                start = validated_data['start_datetime']
                validated_data['end_datetime'] = start + timedelta(hours=1)
        
        # Get attendees data
        attendees_data = validated_data.pop('attendees', [])
        
        # Create event
        event = Event.objects.create(**validated_data)
        
        # Handle attendees
        for attendee_data in attendees_data:
            if 'email' in attendee_data and not attendee_data['email']:
                attendee_data['email'] = None
            Attendee.objects.create(event=event, **attendee_data)
        
        return event

    def update(self, instance, validated_data):
        """Synchronous update method."""
        # Handle end_datetime default logic
        if 'start_datetime' in validated_data and 'end_datetime' not in validated_data:
            if validated_data.get('title') != 'Processing...':
                validated_data['end_datetime'] = validated_data['start_datetime'] + timedelta(hours=1)
        
        # Get attendees data
        attendees_data = validated_data.pop('attendees', None)
        
        # Update event fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle attendees update
        if attendees_data is not None:
            # Delete existing attendees
            instance.attendees.all().delete()
            # Create new attendees
            for attendee_data in attendees_data:
                if 'email' in attendee_data and not attendee_data['email']:
                    attendee_data['email'] = None
                Attendee.objects.create(event=instance, **attendee_data)
        
        return instance

class EventsGroupSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    
    class Meta:
        model = EventsGroup
        fields = [
            'id', 'created_at', 'updated_at', 'use_llm',
            'processing_complete', 'processing_error', 'events'
        ]
        
    def validate(self, data):
        """
        Add any group-level validation here.
        Currently, no specific validation is implemented.
        """
        return data
