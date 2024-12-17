# calendars/api/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CalendarProviderViewSet, UserPreferenceViewSet

router = DefaultRouter()
router.register(r'providers', CalendarProviderViewSet)
router.register(r'preferences', UserPreferenceViewSet)

urlpatterns = router.urls