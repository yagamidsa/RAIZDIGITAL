# Actualizar raizdigital/settings/production.py

from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
]

# Database - Railway PostgreSQL con configuración robusta
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Si Railway proporciona DATABASE_URL (más común)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Configuración manual con variables individuales
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PGDATABASE'),
            'USER': os.environ.get('PGUSER'),
            'PASSWORD': os.environ.get('PGPASSWORD'),
            'HOST': os.environ.get('PGHOST'),
            'PORT': os.environ.get('PGPORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
            'CONN_MAX_AGE': 600,
            'ATOMIC_REQUESTS': True,
        }
    }

# Debug de conexión de base de datos
print("=== DEBUG DATABASE CONFIG ===")
print(f"PGHOST: {os.environ.get('PGHOST')}")
print(f"PGDATABASE: {os.environ.get('PGDATABASE')}")
print(f"PGUSER: {os.environ.get('PGUSER')}")
print(f"DATABASE_URL present: {bool(os.environ.get('DATABASE_URL'))}")

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}