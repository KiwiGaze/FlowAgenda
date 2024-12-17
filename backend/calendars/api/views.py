# calendars/api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from calendars.models import CalendarProvider, EventSync, UserPreference
from calendars.api.serializers import (
    CalendarProviderSerializer,
    EventSyncSerializer,
    UserPreferenceSerializer
)

class CalendarProviderViewSet(viewsets.ModelViewSet):
    queryset = CalendarProvider.objects.all()
    serializer_class = CalendarProviderSerializer
    
    @action(detail=True, methods=['POST'])
    def connect(self, request, pk=None):
        """Handle OAuth connection flow"""
        provider = self.get_object()
        
        try:
            # Here you would implement OAuth flow
            provider.is_connected = True
            provider.save()
            
            return Response({
                'status': 'success',
                'message': f'Successfully connected to {provider.get_name_display()}'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['POST'])
    def disconnect(self, request, pk=None):
        """Disconnect calendar provider"""
        provider = self.get_object()
        
        try:
            provider.is_connected = False
            provider.credentials = {}
            provider.save()
            
            return Response({
                'status': 'success',
                'message': f'Successfully disconnected from {provider.get_name_display()}'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    
    def get_object(self):
        """Get preference by key instead of ID"""
        key = self.kwargs.get('pk')
        return get_object_or_404(UserPreference, key=key)