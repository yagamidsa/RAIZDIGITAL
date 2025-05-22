import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback')
DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
    'raizdigital-production.up.railway.app',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'raizdigital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'raizdigital.wsgi.application'

# Base de datos - CORREGIDO
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
        print(f"🗄️ Usando DATABASE_URL: {DATABASE_URL[:20]}...")
    except ImportError:
        print("❌ dj_database_url no disponible, usando parser manual")
        import re
        match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', DATABASE_URL)
        if match:
            user, password, host, port, database = match.groups()
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': database,
                    'USER': user,
                    'PASSWORD': password,
                    'HOST': host,
                    'PORT': port,
                    'OPTIONS': {'sslmode': 'require'},
                    'CONN_MAX_AGE': 600,
                }
            }
            print(f"🗄️ BD configurada: {user}@{host}:{port}/{database}")
        else:
            print("❌ No se pudo parsear DATABASE_URL")
            raise ValueError("DATABASE_URL inválida")
else:
    # Fallback usando variables individuales de Railway
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PGDATABASE', 'railway'),
            'USER': os.environ.get('PGUSER', 'postgres'),
            'PASSWORD': os.environ.get('PGPASSWORD', ''),
            'HOST': os.environ.get('PGHOST', 'localhost'),
            'PORT': os.environ.get('PGPORT', '5432'),
            'OPTIONS': {'sslmode': 'require'},
            'CONN_MAX_AGE': 600,
        }
    }
    print(f"🗄️ BD configurada con variables individuales: {DATABASES['default']['USER']}@{DATABASES['default']['HOST']}:{DATABASES['default']['PORT']}/{DATABASES['default']['NAME']}")

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Crear directorio staticfiles si no existe
try:
    os.makedirs(STATIC_ROOT, exist_ok=True)
    print(f"📁 STATIC_ROOT creado: {STATIC_ROOT}")
except Exception as e:
    print(f"❌ Error creando STATIC_ROOT: {e}")

static_dir = os.path.join(BASE_DIR, 'static')
if os.path.exists(static_dir):
    STATICFILES_DIRS = [static_dir]
    print(f"📁 STATICFILES_DIRS: {static_dir}")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF Configuration for Railway
CSRF_TRUSTED_ORIGINS = [
    'https://raizdigital-production.up.railway.app',
    'https://raizdigital-production-up.railway.app',
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# Security settings for Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TZ = True

# Session configuration
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

# Logging para debugging
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
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

print('🚀 Railway production settings loaded')