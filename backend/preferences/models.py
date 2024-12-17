# preferences/models.py
from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError

class SystemPreferences(models.Model):
    """
    Singleton model to store system-wide preferences.
    Only one instance of this model can exist.
    """
    theme = models.CharField(
        max_length=10,
        default='system',
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('system', 'System')
        ]
    )
    language = models.CharField(
        max_length=10,
        default='en',
        choices=[
            ('en', 'English'),
            ('zh-CN', 'Simplified Chinese'),
            ('zh-TW', 'Traditional Chinese')
        ]
    )
    model_settings = models.JSONField(
        default=dict,
        help_text='Store model preferences like selected model, base URL etc.'
    )
    ollama_settings = models.JSONField(
        default=dict,
        help_text='Store Ollama-specific settings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'System Preferences'
        verbose_name_plural = 'System Preferences'

    def save(self, *args, **kwargs):
        """Ensure only one instance exists"""
        if SystemPreferences.objects.exists() and not self.pk:
            raise ValidationError('Only one SystemPreferences instance can exist')
        
        # Clear cache on save
        cache.delete('system_preferences')
        return super().save(*args, **kwargs)

    @classmethod
    def get_preferences(cls):
        """
        Get or create the singleton instance with caching
        """
        # Try to get from cache first
        preferences = cache.get('system_preferences')
        if preferences:
            return preferences

        # Default settings matching frontend defaults
        default_settings = {
            'theme': 'system',
            'language': 'en',
            'model_settings': {
                'selectedModel': 'gpt4o',  # Updated to match frontend
                'baseUrl': 'https://api.openai.com/v1'
            },
            'ollama_settings': {
                'baseUrl': 'http://localhost:11434',
                'selectedModel': 'qwen2'  # Updated to match frontend
            }
        }

        # If not in cache, get or create from database
        preferences, created = cls.objects.get_or_create(
            pk=1,
            defaults=default_settings
        )

        # Store in cache for future requests
        cache.set('system_preferences', preferences, timeout=3600)  # Cache for 1 hour
        return preferences
