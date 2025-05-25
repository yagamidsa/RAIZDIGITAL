import os
import sys
from pathlib import Path

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

# 🔧 CONFIGURACIÓN MEJORADA DE ALLOWED_HOSTS PARA RAILWAY
ALLOWED_HOSTS = [
    '*',  # Permitir todos los hosts (para desarrollo)
    '.railway.app',  # Todos los subdominios de railway.app
    '.up.railway.app',  # Todos los subdominios de up.railway.app
    'raizdigital-production.up.railway.app',  # Tu dominio específico
    'localhost',
    '127.0.0.1',
]

# 🔧 DETECTAR Y AGREGAR EL HOST DINÁMICAMENTE
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
# BASE DE DATOS - CONFIGURACIÓN HÍBRIDA
# =================================

print("🗄️  CONFIGURANDO BASE DE DATOS RAILWAY...")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"🔍 DATABASE_URL presente: {'SÍ' if DATABASE_URL else 'NO'}")

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
        
        # Configuración básica
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
        
        # Configuración de conexión
        DATABASES['default']['CONN_MAX_AGE'] = 600
        
        # CONFIGURACIÓN HÍBRIDA: Detectar si estamos en Railway
        is_railway = os.environ.get('RAILWAY_ENVIRONMENT_NAME') is not None
        
        if is_railway:
            # EN RAILWAY: Usar transacciones automáticas
            DATABASES['default']['ATOMIC_REQUESTS'] = True
            print("🚂 RAILWAY detectado: ATOMIC_REQUESTS=True")
        else:
            # LOCAL/OTROS: Transacciones manuales
            DATABASES['default']['ATOMIC_REQUESTS'] = False
            print("🏠 Entorno local: ATOMIC_REQUESTS=False")
        
        # Timeouts básicos
        DATABASES['default']['OPTIONS'].update({
            'connect_timeout': 10,
        })
        
        # Mostrar info de conexión
        db_info = DATABASES['default']
        atomic_status = DATABASES['default']['ATOMIC_REQUESTS']
        print(f"🐘 BD: {db_info['USER']}@{db_info['HOST']}:{db_info['PORT']}/{db_info['NAME']}")
        print(f"📊 ATOMIC_REQUESTS: {atomic_status}")
        
    except ImportError:
        print("❌ dj_database_url no disponible")
        sys.exit(1)
else:
    print("❌ DATABASE_URL no encontrada")
    sys.exit(1)

# Resto de configuración...
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
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# =================================

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT.mkdir(exist_ok=True)

STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 🔧 CONFIGURACIÓN CRUCIAL: WhiteNoise para servir archivos multimedia
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# 🔧 ARCHIVOS MULTIMEDIA - INTEGRADOS CON WHITENOISE
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'staticfiles' / 'media'  # ✅ Dentro de staticfiles para WhiteNoise

# Crear directorios necesarios
MEDIA_ROOT.mkdir(exist_ok=True, parents=True)
(MEDIA_ROOT / 'news').mkdir(exist_ok=True, parents=True)

# 🔧 CONFIGURACIÓN CRÍTICA DE WHITENOISE PARA MULTIMEDIA
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'ico']

# 🔧 PERMITIR QUE WHITENOISE SIRVA ARCHIVOS MULTIMEDIA
WHITENOISE_ROOT = STATIC_ROOT
WHITENOISE_INDEX_FILE = True

print(f"📁 MEDIA_ROOT: {MEDIA_ROOT}")
print(f"📁 STATIC_ROOT: {STATIC_ROOT}")
print(f"🌐 MEDIA_URL: {MEDIA_URL}")
print(f"📦 WhiteNoise configurado para servir multimedia")

# 🔧 VERIFICAR QUE LOS DIRECTORIOS EXISTEN AL INICIO
try:
    STATIC_ROOT.mkdir(exist_ok=True)
    MEDIA_ROOT.mkdir(exist_ok=True, parents=True)
    (MEDIA_ROOT / 'news').mkdir(exist_ok=True, parents=True)
    print("✅ Directorios de archivos creados correctamente")
except Exception as e:
    print(f"❌ Error creando directorios: {e}")

# 🔧 CSRF MEJORADO PARA RAILWAY
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://raizdigital-production.up.railway.app',
    'http://raizdigital-production.up.railway.app',  # Para HTTP también
]

# Agregar dinámicamente si hay variables de Railway
if railway_host:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{railway_host}',
        f'http://{railway_host}',
    ])

print(f"🔒 CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")

# 🔧 CONFIGURACIÓN DE SEGURIDAD AJUSTADA PARA RAILWAY
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway maneja esto
USE_TZ = True

# 🔧 CONFIGURACIÓN DE SESIONES OPTIMIZADA
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False  # Railway puede usar HTTP en algunos casos
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# 🔧 LOGGING MEJORADO PARA DEBUGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
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
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔧 CONFIGURACIÓN ADICIONAL PARA DEBUGGING
print('🚀 PRODUCTION SETTINGS CARGADOS CORRECTAMENTE')
print(f'🌐 HOST ESPERADO: raizdigital-production.up.railway.app')
print(f'🔒 CSRF configurado para Railway')
print('=' * 60)
