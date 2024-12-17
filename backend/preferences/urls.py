# preferences/urls.py
from django.urls import path, include
from .views import SystemPreferencesView

# Version 1 URL patterns
v1_patterns = [
    path('preferences/', SystemPreferencesView.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'put': 'update'
    }), name='system-preferences'),
    path('preferences/sync/', SystemPreferencesView.as_view({
        'post': 'sync'
    }), name='preferences-sync'),
]

# Main URL patterns with versioning
urlpatterns = [
    path('v1/', include((v1_patterns, 'v1'), namespace='v1-preferences')),
]