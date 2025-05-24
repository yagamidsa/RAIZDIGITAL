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

# ALLOWED_HOSTS - Permitir todos para Railway
ALLOWED_HOSTS = ['*']
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
# BASE DE DATOS - CONFIGURACIÓN MINIMALISTA
# =================================

print("🗄️  CONFIGURANDO BASE DE DATOS RAILWAY...")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"🔍 DATABASE_URL presente: {'SÍ' if DATABASE_URL else 'NO'}")

if DATABASE_URL:
    try:
        # Método 1: Intentar con dj_database_url
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
        
        # CONFIGURACIÓN MINIMALISTA - SOLO LO ESENCIAL
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
        
        # Configuración básica
        DATABASES['default']['CONN_MAX_AGE'] = 60  # Reducido para evitar problemas
        
        db_info = DATABASES['default']
        print(f"🐘 RAILWAY BD (dj_database_url): {db_info['USER']}@{db_info['HOST']}:{db_info['PORT']}/{db_info['NAME']}")
        
    except ImportError:
        # Método 2: Configuración manual sin dj_database_url
        print("📦 dj_database_url no disponible - usando configuración manual")
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
                    },
                    'CONN_MAX_AGE': 60,
                }
            }
            print(f"🐘 BD Manual: {url.username}@{url.hostname}:{url.port}/{url.path[1:]}")
        else:
            print("❌ DATABASE_URL no encontrada")
            sys.exit(1)
            
except Exception as e:
    print(f"❌ Error configurando BD: {e}")
    sys.exit(1)
else:
    print("❌ DATABASE_URL no encontrada en variables de entorno")
    sys.exit(1)

# Validaciones de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración regional
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# =================================
# ARCHIVOS ESTÁTICOS - CONFIGURACIÓN SIMPLE
# =================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Crear directorio si no existe
try:
    STATIC_ROOT.mkdir(exist_ok=True)
    print(f"📂 STATIC_ROOT creado: {STATIC_ROOT}")
except Exception as e:
    print(f"⚠️ Error creando STATIC_ROOT: {e}")

# Directorios de archivos estáticos
STATICFILES_DIRS = []
static_dir = BASE_DIR / 'static'
if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)
    print(f"📁 Static dir encontrado: {static_dir}")

# Configuración básica de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

print(f"📂 STATIC_ROOT: {STATIC_ROOT}")
print(f"📂 STATICFILES_DIRS: {STATICFILES_DIRS}")

# =================================
# SEGURIDAD Y COOKIES
# =================================

# CSRF para Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# Headers de seguridad para Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway maneja SSL

# Configuración de sesiones básica
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True

# Solo aplicar configuración segura de cookies si estamos en HTTPS
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True

# Configuración básica de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',  # Solo warnings y errores
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print('🚀 PRODUCTION SETTINGS MINIMALISTAS CARGADOS')
print('✅ Configuración lista para Railway')
print('=' * 60)