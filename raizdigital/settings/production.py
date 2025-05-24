import os
import sys
from pathlib import Path

# VERIFICAR QUE ESTAMOS EN PRODUCTION.PY
print("🚨 ARCHIVO: production.py SIENDO USADO")
print("🚨 SETTINGS MODULE: raizdigital.settings.production")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    print("❌ CRITICAL: SECRET_KEY no encontrada")
    sys.exit(1)

DEBUG = False
print(f"🔧 DEBUG mode: {DEBUG}")

# ALLOWED_HOSTS - Solución definitiva
ALLOWED_HOSTS = ['*']  # Permitir todos temporalmente
print(f"🌐 ALLOWED_HOSTS: {ALLOWED_HOSTS}")

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

# =================================
# BASE DE DATOS - RAILWAY CORREGIDA
# =================================

print("🗄️  CONFIGURANDO BASE DE DATOS RAILWAY...")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"🔍 DATABASE_URL presente: {'SÍ' if DATABASE_URL else 'NO'}")

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
        
        # CONFIGURACIÓN CORREGIDA - Solo opciones válidas para PostgreSQL
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
            'options': '-c default_transaction_isolation=read_committed',
            # Opciones válidas para psycopg
            'connect_timeout': 10,
            'keepalives_idle': 600,
            'keepalives_interval': 30,
            'keepalives_count': 3,
        }
        
        # Configuración de conexión
        DATABASES['default']['CONN_MAX_AGE'] = 600
        DATABASES['default']['ATOMIC_REQUESTS'] = True
        
        # Mostrar info de conexión (sin datos sensibles)
        db_info = DATABASES['default']
        print(f"🐘 RAILWAY BD: {db_info['USER']}@{db_info['HOST']}:{db_info['PORT']}/{db_info['NAME']}")
        
    except ImportError:
        print("❌ dj_database_url no disponible - instalando...")
        # Si dj_database_url no está disponible, usar configuración manual
        import urllib.parse as urlparse
        
        if DATABASE_URL:
            url = urlparse.urlparse(DATABASE_URL)
            
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': url.path[1:],
                    'USER': url.username,
                    'PASSWORD': url.password,
                    'HOST': url.hostname,
                    'PORT': url.port,
                    'OPTIONS': {
                        'sslmode': 'require',
                        'connect_timeout': 10,
                    },
                    'CONN_MAX_AGE': 600,
                    'ATOMIC_REQUESTS': True,
                }
            }
            print(f"🐘 BD Manual: {url.username}@{url.hostname}:{url.port}/{url.path[1:]}")
        else:
            print("❌ DATABASE_URL no encontrada")
            sys.exit(1)
else:
    print("❌ DATABASE_URL no encontrada")
    sys.exit(1)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos - CONFIGURACIÓN MEJORADA
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Crear directorio si no existe
STATIC_ROOT.mkdir(exist_ok=True)

# Directorios de archivos estáticos
STATICFILES_DIRS = []
static_dir = BASE_DIR / 'static'
if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)
    print(f"📁 Static dir agregado: {static_dir}")

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

print(f"📂 STATIC_ROOT: {STATIC_ROOT}")
print(f"📂 STATICFILES_DIRS: {STATICFILES_DIRS}")

# CSRF y Seguridad
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# Configuración de seguridad para Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway maneja SSL
USE_TZ = True

# Configuración de sesiones
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Configuración de cookies
SESSION_COOKIE_SECURE = True  # Solo HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print('🚀 PRODUCTION SETTINGS CARGADOS CORRECTAMENTE')
print('=' * 60)