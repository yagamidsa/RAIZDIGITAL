import os
import sys
from pathlib import Path

print("🚨 ARCHIVO: production.py - CORREGIDO PARA RAILWAY")
print("🚨 SETTINGS MODULE: raizdigital.settings.production")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    print("❌ CRITICAL: SECRET_KEY no encontrada")
    sys.exit(1)

DEBUG = False
print(f"🔧 DEBUG mode: {DEBUG}")

# ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '*',
    '.railway.app',
    '.up.railway.app',
    'raizdigital-production.up.railway.app',
    'localhost',
    '127.0.0.1',
]

railway_host = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if railway_host:
    ALLOWED_HOSTS.append(railway_host)
    print(f"🌐 Railway host detectado: {railway_host}")

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

# 🔧 MIDDLEWARE CORREGIDO
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # DEBE SER SEGUNDO
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AuthenticationMiddleware',
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
                'core.context_processors.media_url',
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
        
        # 🔧 CONFIGURACIÓN CORREGIDA PARA RAILWAY
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
            'connect_timeout': 10,
            'options': '-c default_transaction_isolation=read_committed'
        }
        
        DATABASES['default']['CONN_MAX_AGE'] = 600
        DATABASES['default']['ATOMIC_REQUESTS'] = True
        
        # 🔧 CONFIGURACIÓN ADICIONAL PARA ESTABILIDAD
        DATABASES['default']['CONN_HEALTH_CHECKS'] = True
        
        print("🚂 RAILWAY: Configuración de BD optimizada")
        
        db_info = DATABASES['default']
        print(f"🐘 BD: {db_info['USER']}@{db_info['HOST']}:{db_info['PORT']}/{db_info['NAME']}")
        print(f"📊 ATOMIC_REQUESTS: {DATABASES['default']['ATOMIC_REQUESTS']}")
        
    except ImportError:
        print("❌ dj_database_url no disponible")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        sys.exit(1)
else:
    print("❌ DATABASE_URL no encontrada")
    sys.exit(1)

# Password validation
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

# =================================
# 🔧 ARCHIVOS ESTÁTICOS - RAILWAY CORREGIDO
# =================================

print("📁 CONFIGURANDO ARCHIVOS ESTÁTICOS PARA RAILWAY...")

# URLs y directorios básicos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔧 STATICFILES_DIRS - Solo directorios adicionales necesarios
STATICFILES_DIRS = []

# Verificar si existe directorio static/ adicional
project_static_dir = BASE_DIR / 'static'
if project_static_dir.exists() and str(project_static_dir) != str(STATIC_ROOT):
    STATICFILES_DIRS.append(str(project_static_dir))
    print(f"📁 Directorio static/ adicional: {project_static_dir}")

# Finders en orden correcto
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 🔧 WHITENOISE CONFIGURACIÓN OPTIMIZADA
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración WhiteNoise específica
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = False
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'ico', 
    'mp4', 'webm', 'mp3', 'wav', 'ogg'
]
WHITENOISE_MAX_AGE = 31536000  # 1 año
WHITENOISE_ADD_HEADERS_FUNCTION = 'raizdigital.settings.production.custom_headers'

def custom_headers(headers, path, url):
    """Headers personalizados para diferentes tipos de archivos"""
    if path.endswith('.css'):
        headers['Content-Type'] = 'text/css; charset=utf-8'
        headers['Cache-Control'] = 'public, max-age=31536000'
    elif path.endswith('.js'):
        headers['Content-Type'] = 'application/javascript; charset=utf-8'
        headers['Cache-Control'] = 'public, max-age=31536000'
    elif path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        headers['Cache-Control'] = 'public, max-age=31536000'
    return headers

# Crear STATIC_ROOT
try:
    STATIC_ROOT.mkdir(exist_ok=True, parents=True)
    print(f"✅ STATIC_ROOT: {STATIC_ROOT}")
except Exception as e:
    print(f"❌ Error creando STATIC_ROOT: {e}")

# =================================
# 🔧 ARCHIVOS MULTIMEDIA - RAILWAY CORREGIDO
# =================================

print("📸 CONFIGURANDO ARCHIVOS MULTIMEDIA...")

# 🔧 DETECTAR RAILWAY VOLUME CORRECTAMENTE
railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
print(f"🔍 RAILWAY_VOLUME_MOUNT_PATH: {railway_volume}")

# Verificar si es un volumen válido (no el de postgres)
valid_volume = (
    railway_volume and 
    railway_volume != '/var/lib/postgresql/data' and
    railway_volume != '/app/media' and  # ❌ Este era el problema
    os.path.exists(railway_volume) if railway_volume else False
)

print(f"🔍 Volume válido: {valid_volume}")

if valid_volume:
    # ✅ VOLUMEN PERSISTENTE VÁLIDO
    MEDIA_ROOT = Path(railway_volume) / 'media'
    MEDIA_URL = '/media/'
    print(f"💾 ✅ Volume persistente válido: {MEDIA_ROOT}")
    
    try:
        MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        (MEDIA_ROOT / 'news').mkdir(exist_ok=True)
        print(f"✅ Directorios de media creados en volume")
    except Exception as e:
        print(f"⚠️ Error creando directorios en volume: {e}")
        # Fallback a temporal
        valid_volume = False

if not valid_volume:
    # ❌ SIN VOLUMEN VÁLIDO - USAR ALMACENAMIENTO TEMPORAL
    MEDIA_ROOT = STATIC_ROOT / 'temp_media'
    MEDIA_URL = '/static/temp_media/'
    print(f"📁 ⚠️ Almacenamiento temporal: {MEDIA_ROOT}")
    
    try:
        MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        (MEDIA_ROOT / 'news').mkdir(exist_ok=True)
        print(f"✅ Directorios de media temporales creados")
    except Exception as e:
        print(f"❌ Error creando directorios temporales: {e}")

# =================================
# 🔧 CONFIGURACIÓN DE SEGURIDAD CORREGIDA
# =================================

# CSRF Origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://raizdigital-production.up.railway.app',
]

if railway_host:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{railway_host}',
        f'http://{railway_host}',
    ])

# 🔧 CONFIGURACIÓN DE SEGURIDAD RAILWAY
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway maneja SSL automáticamente
USE_TZ = True

# 🔧 CONFIGURACIÓN DE SESIONES ESTABLE
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False  # Railway maneja HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# 🔧 CACHE OPTIMIZADO PARA RAILWAY
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'raizdigital-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 2000,
            'CULL_FREQUENCY': 3,
        },
        'TIMEOUT': 300,  # 5 minutos
    }
}

# =================================
# 🔧 LOGGING OPTIMIZADO PARA RAILWAY
# =================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
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
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # Reducir logs de BD
            'propagate': False,
        },
        'django.contrib.staticfiles': {
            'handlers': ['console'],
            'level': 'WARNING',  # Reducir logs de archivos estáticos
            'propagate': False,
        },
        'whitenoise': {
            'handlers': ['console'],
            'level': 'WARNING',  # Reducir logs de WhiteNoise
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =================================
# 🔧 CONFIGURACIÓN ADICIONAL RAILWAY
# =================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔧 CONFIGURACIÓN DE EMAIL (si es necesario)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 🔧 CONFIGURACIÓN DE ARCHIVOS SUBIDOS
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# 🔧 TIMEOUT CONFIGURACIONES
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# =================================
# 🔧 RESUMEN FINAL DE CONFIGURACIÓN
# =================================

print("\n📊 RESUMEN DE CONFIGURACIÓN RAILWAY:")
print(f"   DEBUG: {DEBUG}")
print(f"   STATIC_URL: {STATIC_URL}")
print(f"   STATIC_ROOT: {STATIC_ROOT}")
print(f"   MEDIA_URL: {MEDIA_URL}")
print(f"   MEDIA_ROOT: {MEDIA_ROOT}")
print(f"   STATICFILES_STORAGE: {STATICFILES_STORAGE}")
print(f"   RAILWAY_VOLUME: {railway_volume}")
print(f"   VOLUME_VÁLIDO: {valid_volume}")

# Verificar archivos críticos
critical_dirs = [STATIC_ROOT, MEDIA_ROOT]
for directory in critical_dirs:
    if directory.exists():
        print(f"   ✅ {directory.name}: EXISTE")
    else:
        print(f"   ❌ {directory.name}: NO EXISTE")

print('\n🚀 PRODUCTION SETTINGS CORREGIDO PARA RAILWAY')
print('🔧 ERRORES DE VOLUMEN Y BD SOLUCIONADOS')
print('=' * 60)