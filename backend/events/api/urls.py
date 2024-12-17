# events/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet,
    EventsGroupViewSet,
    llm_config_view,
    global_search,
    get_ollama_models,
    check_ollama_status,
)

# Create versioned routers
v1_router = DefaultRouter()
v1_router.register(r'events', EventViewSet, basename='event')
v1_router.register(r'groups', EventsGroupViewSet, basename='events-group')

# Version 1 URL patterns
v1_patterns = [

    # Create from text endpoint
    path('groups/create-from-text/', 
         EventsGroupViewSet.as_view({'post': 'create_from_text'}),
         name='events-create-from-text'),

    # Router URLs
    path('', include(v1_router.urls)),
    
    # Additional endpoints
    path('llm-config/', llm_config_view, name='llm-config'),
    
    # Search endpoint - only need one pattern
    path('search/', global_search, name='global-search'),

    # Ollama endpoints
    path('ollama/models/', get_ollama_models, name='ollama-models'),
    path('ollama/status/', check_ollama_status, name='ollama-status'),
    
]

# Main URL patterns with versioning
urlpatterns = [
    path('v1/', include((v1_patterns, 'v1'))),
]