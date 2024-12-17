# preferences/admin.py
from django.contrib import admin
from .models import SystemPreferences

@admin.register(SystemPreferences)
class SystemPreferencesAdmin(admin.ModelAdmin):
    list_display = ('theme', 'language', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Prevent creating additional instances
        return not SystemPreferences.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the singleton instance
        return False