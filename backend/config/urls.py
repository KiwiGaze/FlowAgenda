# config/urls.py
from django.contrib import admin
from django.urls import path, include
from events.api.urls import urlpatterns as events_urls
from preferences.urls import urlpatterns as preferences_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(events_urls)),
    path('api/', include(preferences_urls)),
]