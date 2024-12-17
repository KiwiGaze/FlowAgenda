# config/settings/local.py

# Override DEBUG
DEBUG = True

# Add development-specific apps
INSTALLED_APPS += ['debug_toolbar']

# Use different database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev.sqlite3',
    }
}

# Override secret key
SECRET_KEY = 'your-development-secret-key'

# Add development-specific middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'