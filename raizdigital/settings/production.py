import os
import sys
from pathlib import Path

print("🚨 ARCHIVO: production.py SIENDO USADO - CORREGIDO PARA MÓVIL")
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

# 🔧 MIDDLEWARE CORREGIDO PARA WHITENOISE
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
# BASE DE DATOS - RAILWAY
# =================================

print("🗄️  CONFIGURANDO BASE DE DATOS RAILWAY...")

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"🔍 DATABASE_URL presente: {'SÍ' if DATABASE_URL else 'NO'}")

if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
        
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
        
        DATABASES['default']['CONN_MAX_AGE'] = 600
        
        is_railway = os.environ.get('RAILWAY_ENVIRONMENT_NAME') is not None
        
        if is_railway:
            DATABASES['default']['ATOMIC_REQUESTS'] = True
            print("🚂 RAILWAY detectado: ATOMIC_REQUESTS=True")
        else:
            DATABASES['default']['ATOMIC_REQUESTS'] = False
            print("🏠 Entorno local: ATOMIC_REQUESTS=False")
        
        DATABASES['default']['OPTIONS'].update({
            'connect_timeout': 10,
        })
        
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
# 🔧 CONFIGURACIÓN ARCHIVOS ESTÁTICOS CORREGIDA PARA MÓVIL
# =================================

print("📁 CONFIGURANDO ARCHIVOS ESTÁTICOS PARA MÓVIL...")

# URLs y directorios
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔧 CONFIGURACIÓN STATICFILES_DIRS CORREGIDA
STATICFILES_DIRS = []

# Verificar estructura de archivos estáticos
core_static_dir = BASE_DIR / 'core' / 'static'
project_static_dir = BASE_DIR / 'static'

print(f"🔍 Verificando core/static/: {core_static_dir.exists()}")
print(f"🔍 Verificando project static/: {project_static_dir.exists()}")

# Solo agregar a STATICFILES_DIRS si existe y no es el STATIC_ROOT
if project_static_dir.exists() and str(project_static_dir) != str(STATIC_ROOT):
    STATICFILES_DIRS.append(str(project_static_dir))
    print(f"📁 Agregado a STATICFILES_DIRS: {project_static_dir}")

# Finders en orden correcto
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',  # Para STATICFILES_DIRS
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # Para core/static/
]

# 🔧 CONFIGURACIÓN WHITENOISE OPTIMIZADA PARA MÓVIL
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración WhiteNoise específica para móvil
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = False
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'ico', 
    'mp4', 'webm', 'mp3', 'wav', 'ogg'
]
WHITENOISE_MAX_AGE = 31536000  # 1 año
WHITENOISE_ADD_HEADERS_FUNCTION = 'raizdigital.settings.production.custom_headers'

# 🔧 FUNCIÓN PARA HEADERS PERSONALIZADOS
def custom_headers(headers, path, url):
    """Agregar headers específicos para diferentes tipos de archivos"""
    if path.endswith('.css'):
        headers['Content-Type'] = 'text/css; charset=utf-8'
        headers['Cache-Control'] = 'public, max-age=31536000'
    elif path.endswith('.js'):
        headers['Content-Type'] = 'application/javascript; charset=utf-8'
        headers['Cache-Control'] = 'public, max-age=31536000'
    elif path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        headers['Cache-Control'] = 'public, max-age=31536000'
    return headers

# Crear directorios necesarios
try:
    STATIC_ROOT.mkdir(exist_ok=True, parents=True)
    print(f"✅ STATIC_ROOT creado: {STATIC_ROOT}")
except Exception as e:
    print(f"❌ Error creando STATIC_ROOT: {e}")

# =================================
# ARCHIVOS MULTIMEDIA - CONFIGURACIÓN CORREGIDA
# =================================

print("📸 CONFIGURANDO ARCHIVOS MULTIMEDIA...")

railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
valid_volume = railway_volume and railway_volume != '/var/lib/postgresql/data'

if valid_volume:
    MEDIA_ROOT = Path(railway_volume) / 'media'
    MEDIA_URL = '/media/'
    print(f"💾 ✅ Volume persistente: {MEDIA_ROOT}")
else:
    # Para archivos temporales, usar un subdirectorio de static
    MEDIA_ROOT = STATIC_ROOT / 'temp_media'
    MEDIA_URL = '/static/temp_media/'
    print(f"📁 ⚠️ Almacenamiento temporal: {MEDIA_ROOT}")

# Crear directorios de media
try:
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    (MEDIA_ROOT / 'news').mkdir(exist_ok=True)
    print(f"✅ Directorios de media creados: {MEDIA_ROOT}")
except Exception as e:
    print(f"❌ Error creando directorios media: {e}")

# =================================
# 🔧 CONFIGURACIÓN ADICIONAL PARA MÓVIL
# =================================

# CSRF - Configuración mejorada
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://raizdigital-production.up.railway.app',
    'http://raizdigital-production.up.railway.app',
]

if railway_host:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{railway_host}',
        f'http://{railway_host}',
    ])

# Seguridad optimizada para móvil
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Railway maneja SSL
USE_TZ = True

# 🔧 CONFIGURACIÓN DE CACHE PARA ARCHIVOS ESTÁTICOS
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Sesiones optimizadas
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False  # Railway maneja HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# 🔧 LOGGING MEJORADO PARA DEBUG DE ARCHIVOS ESTÁTICOS
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
        'django.contrib.staticfiles': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'whitenoise': {
            'handlers': ['console'],
            'level': 'DEBUG',
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

# =================================
# 🔧 VERIFICACIÓN FINAL DE ARCHIVOS ESTÁTICOS
# =================================

print("\n📊 RESUMEN DE CONFIGURACIÓN CORREGIDA:")
print(f"   STATIC_URL: {STATIC_URL}")
print(f"   STATIC_ROOT: {STATIC_ROOT}")
print(f"   STATICFILES_DIRS: {STATICFILES_DIRS}")
print(f"   STATICFILES_STORAGE: {STATICFILES_STORAGE}")
print(f"   MEDIA_ROOT: {MEDIA_ROOT}")
print(f"   MEDIA_URL: {MEDIA_URL}")
print(f"   DEBUG: {DEBUG}")

# Verificar archivos CSS específicos
css_files_to_check = [
    'core/css/variables.css',
    'core/css/login.css',
    'core/css/news.css',
]

for css_file in css_files_to_check:
    file_path = core_static_dir / css_file
    if file_path.exists():
        file_size = file_path.stat().st_size
        print(f"   ✅ CSS encontrado: {css_file} ({file_size} bytes)")
    else:
        print(f"   ❌ CSS faltante: {css_file}")

print('\n🚀 PRODUCTION SETTINGS CORREGIDO PARA MÓVIL')
print('=' * 60)