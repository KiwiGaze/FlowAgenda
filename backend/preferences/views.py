# preferences/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SystemPreferences
from .serializers import SystemPreferencesSerializer

class SystemPreferencesView(viewsets.ViewSet):
    def retrieve(self, request):
        """Get system preferences"""
        try:
            preferences = SystemPreferences.get_preferences()
            serializer = SystemPreferencesSerializer(preferences)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 'PREFERENCES_FETCH_ERROR'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request):
        """Update system preferences"""
        try:
            preferences = SystemPreferences.get_preferences()
            serializer = SystemPreferencesSerializer(
                preferences,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'data': serializer.data
                })
            
            return Response({
                'success': False,
                'error': {
                    'message': 'Validation failed',
                    'code': 'VALIDATION_ERROR',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 'PREFERENCES_UPDATE_ERROR'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def sync(self, request):
        """Force sync preferences"""
        try:
            preferences = SystemPreferences.get_preferences()
            serializer = SystemPreferencesSerializer(
                preferences,
                data=request.data,
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'data': serializer.data
                })
            
            return Response({
                'success': False,
                'error': {
                    'message': 'Sync validation failed',
                    'code': 'SYNC_VALIDATION_ERROR',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 'PREFERENCES_SYNC_ERROR'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)