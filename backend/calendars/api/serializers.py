# calendars/api/serializers.py
from rest_framework import serializers
from calendars.models import CalendarProvider, EventSync, UserPreference

class CalendarProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarProvider
        fields = [
            'id', 'name', 'is_connected', 'last_synced',
            'settings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_connected', 'last_synced']

class EventSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSync
        fields = [
            'id', 'event', 'provider', 'provider_event_id',
            'last_synced', 'sync_status'
        ]
        read_only_fields = ['last_synced', 'sync_status']

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['id', 'key', 'value', 'updated_at']
        read_only_fields = ['updated_at']