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
# ARCHIVOS ESTÁTICOS Y MULTIMEDIA - CONFIGURACIÓN CORREGIDA PARA EVITAR CONFLICTOS
# =================================

# 🔧 CONFIGURACIÓN BASE DE ARCHIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔧 CREAR DIRECTORIOS BASE
STATIC_ROOT.mkdir(exist_ok=True)

# 🔧 STATICFILES_DIRS INICIAL (vacío para evitar conflictos)
STATICFILES_DIRS = []

# Agregar directorio static del proyecto si existe (pero no conflictúe)
project_static = BASE_DIR / 'static'
if project_static.exists() and project_static != STATIC_ROOT:
    STATICFILES_DIRS.append(str(project_static))

# 🔧 CONFIGURACIÓN DE ARCHIVOS MULTIMEDIA CORREGIDA
# Verificar todas las variables de volumen posibles
RAILWAY_VOLUME_PATHS = [
    os.environ.get('RAILWAY_VOLUME_MOUNT_PATH'),
    os.environ.get('VOLUME_MOUNT_PATH'),
    os.environ.get('RAILWAY_MEDIA_VOLUME'),
    os.environ.get('MEDIA_VOLUME'),
]

# Encontrar el primer path válido
RAILWAY_VOLUME_PATH = None
for path in RAILWAY_VOLUME_PATHS:
    if path and path != '/var/lib/postgresql/data':  # Excluir volumen de postgres
        RAILWAY_VOLUME_PATH = path
        break

print(f"🔍 VARIABLES DE VOLUMEN VERIFICADAS:")
for i, path in enumerate(RAILWAY_VOLUME_PATHS):
    var_names = ['RAILWAY_VOLUME_MOUNT_PATH', 'VOLUME_MOUNT_PATH', 'RAILWAY_MEDIA_VOLUME', 'MEDIA_VOLUME']
    valid = path and path != '/var/lib/postgresql/data'
    print(f"   {var_names[i]}: {path or 'NO CONFIGURADA'} {'✅' if valid else '❌'}")

if RAILWAY_VOLUME_PATH:
    # ✅ USANDO RAILWAY VOLUME CORRECTO
    MEDIA_ROOT = Path(RAILWAY_VOLUME_PATH) / 'media'
    MEDIA_URL = '/media/'
    
    # Crear directorios necesarios en el volumen persistente
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    (MEDIA_ROOT / 'news').mkdir(exist_ok=True)
    (MEDIA_ROOT / 'profiles').mkdir(exist_ok=True)
    
    # 🔧 CONFIGURACIÓN WHITENOISE CORREGIDA
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'ico']
    
    # 🔧 CRITICAL FIX: NO agregar MEDIA_ROOT a STATICFILES_DIRS para evitar conflictos
    # En su lugar, Django servirá archivos multimedia de forma separada
    
    print(f"💾 ✅ RAILWAY VOLUME CONFIGURADO CORRECTAMENTE")
    print(f"📁 MEDIA_ROOT (persistente): {MEDIA_ROOT}")
    print(f"🔗 MEDIA_URL: {MEDIA_URL}")
    
else:
    # ❌ NO HAY VOLUMEN VÁLIDO - USAR FALLBACK TEMPORAL CORREGIDO
    print(f"⚠️ NO SE DETECTÓ VOLUMEN VÁLIDO - USANDO ALMACENAMIENTO TEMPORAL")
    
    # 🔧 CREAR DIRECTORIO SEPARADO PARA MEDIA DENTRO DE STATICFILES
    media_temp_dir = STATIC_ROOT / 'temp_media'
    media_temp_dir.mkdir(parents=True, exist_ok=True)
    (media_temp_dir / 'news').mkdir(exist_ok=True)
    
    MEDIA_ROOT = media_temp_dir
    MEDIA_URL = '/static/temp_media/'
    
    print(f"📁 MEDIA_ROOT (temporal): {MEDIA_ROOT}")
    print(f"🚨 Las imágenes se borrarán en cada deploy")
    print(f"🔗 MEDIA_URL: {MEDIA_URL}")

# 🔧 CONFIGURACIÓN STATICFILES FINAL
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# 🔧 VERIFICAR CONFIGURACIÓN FINAL
print(f"\n📊 CONFIGURACIÓN FINAL DE ARCHIVOS:")
print(f"   STATIC_ROOT: {STATIC_ROOT}")
print(f"   STATICFILES_DIRS: {STATICFILES_DIRS}")
print(f"   MEDIA_ROOT: {MEDIA_ROOT}")
print(f"   MEDIA_URL: {MEDIA_URL}")
print(f"   Persistente: {'SÍ ✅' if RAILWAY_VOLUME_PATH else 'NO ❌'}")

# Verificar que no hay conflictos
conflict_check = str(MEDIA_ROOT) in [str(STATIC_ROOT)] + [str(d) for d in STATICFILES_DIRS]
if conflict_check:
    print(f"⚠️ ADVERTENCIA: Posible conflicto en configuración de archivos")
else:
    print(f"✅ No hay conflictos en configuración de archivos")

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

# 🔧 CREAR DIRECTORIOS AL FINAL PARA ASEGURAR QUE EXISTEN
try:
    STATIC_ROOT.mkdir(exist_ok=True)
    MEDIA_ROOT.mkdir(exist_ok=True, parents=True)
    (MEDIA_ROOT / 'news').mkdir(exist_ok=True, parents=True)
    print("✅ Directorios creados correctamente")
except Exception as e:
    print(f"❌ Error creando directorios: {e}")

print('🚀 PRODUCTION SETTINGS CARGADOS CORRECTAMENTE')
print(f'🌐 HOST ESPERADO: raizdigital-production.up.railway.app')
print(f'🔒 CSRF configurado para Railway')
print('=' * 60)