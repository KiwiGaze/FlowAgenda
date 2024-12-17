# events/services/llm_config.py
import json
import os
from pathlib import Path
from django.conf import settings
from typing import Dict, Any

class LLMConfig:
    """Configuration manager for LLM services"""
    
    def __init__(self):
        self.llm_provider = settings.LLM_PROVIDER if settings.LLM_PROVIDER else 'openai' # Default to OpenAI

        self.openai_api_key = settings.OPENAI_API_KEY if settings.OPENAI_API_KEY else "Enter your OpenAI API key here"
        self.openai_model = settings.OPENAI_MODEL if settings.OPENAI_MODEL else "Enter your OpenAI model here"

        self.google_api_key = settings.GOOGLE_API_KEY if settings.GOOGLE_API_KEY else "Enter your Google API key here"
        self.google_model = settings.GOOGLE_MODEL if settings.GOOGLE_MODEL else "Enter your Google model here"

        self.deepseek_api_key = settings.DEEPSEEK_API_KEY if settings.DEEPSEEK_API_KEY else "Enter your DEEPSEEK API key here"
        self.deepseek_model = settings.DEEPSEEK_MODEL if settings.DEEPSEEK_MODEL else "Enter your DEEPSEEK model here"

        self.alibaba_api_key = settings.ALIBABA_API_KEY if settings.ALIBABA_API_KEY else "Enter your Alibaba API key here"
        self.alibaba_model = settings.ALIBABA_MODEL if settings.ALIBABA_MODEL else "Enter your Alibaba model here"
