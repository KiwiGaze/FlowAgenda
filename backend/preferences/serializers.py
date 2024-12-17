# preferences/serializers.py
from rest_framework import serializers
from .models import SystemPreferences

class ModelSettingsSerializer(serializers.Serializer):
    selectedModel = serializers.CharField(required=True)
    baseUrl = serializers.URLField(required=True)

class OllamaSettingsSerializer(serializers.Serializer):
    baseUrl = serializers.URLField(required=True)
    selectedModel = serializers.CharField(required=True)

class SystemPreferencesSerializer(serializers.ModelSerializer):
    model_settings = ModelSettingsSerializer()
    ollama_settings = OllamaSettingsSerializer()

    class Meta:
        model = SystemPreferences
        fields = [
            'theme', 
            'language', 
            'model_settings',
            'ollama_settings',
            'updated_at'
        ]
        read_only_fields = ['updated_at']

    def validate_theme(self, value):
        """Validate theme value"""
        valid_themes = {'light', 'dark', 'system'}
        if value not in valid_themes:
            raise serializers.ValidationError(
                f"Theme must be one of: {', '.join(valid_themes)}"
            )
        return value

    def validate_language(self, value):
        """Validate language value"""
        valid_languages = {'en', 'zh-CN', 'zh-TW'}
        if value not in valid_languages:
            raise serializers.ValidationError(
                f"Language must be one of: {', '.join(valid_languages)}"
            )
        return value

    def update(self, instance, validated_data):
        """Handle nested updates"""
        if 'model_settings' in validated_data:
            instance.model_settings.update(validated_data.pop('model_settings'))

        if 'ollama_settings' in validated_data:
            instance.ollama_settings.update(validated_data.pop('ollama_settings'))

        return super().update(instance, validated_data)