import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY con mejor manejo de errores
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    print("❌ CRITICAL: SECRET_KEY no encontrada en variables de entorno")
    print("💡 Configura SECRET_KEY en Railway")
    sys.exit(1)

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
print(f"🔧 DEBUG mode: {DEBUG}")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
]

# También permitir el dominio específico si existe
railway_domain = os.environ.get('RAILWAY_STATIC_URL')
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain.replace('https://', '').replace('http://', ''))

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

# Base de datos con mejor manejo de errores
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {}

if DATABASE_URL:
    print(f"🗄️  Usando DATABASE_URL")
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
        print("✅ Base de datos configurada con dj_database_url")
    except ImportError:
        print("⚠️  dj_database_url no disponible, usando parser manual")
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
            print(f"✅ BD configurada manualmente: {user}@{host}:{port}/{database}")
        else:
            print("❌ ERROR: No se pudo parsear DATABASE_URL")
            raise ValueError("DATABASE_URL tiene formato inválido")
else:
    # Usar variables individuales
    print("🗄️  Usando variables de entorno individuales")
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
    db_config = DATABASES['default']
    print(f"✅ BD configurada: {db_config['USER']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}")

# Verificar que tenemos configuración de BD
if not DATABASES.get('default'):
    print("❌ CRITICAL: No se pudo configurar la base de datos")
    print("💡 Verifica las variables DATABASE_URL o PG* en Railway")
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

# =================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS - CORREGIDA PARA TU ESTRUCTURA
# =================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Crear directorio staticfiles
STATIC_ROOT.mkdir(exist_ok=True)
print(f"📁 STATIC_ROOT: {STATIC_ROOT}")

# STATICFILES_DIRS - Configuración correcta para tu estructura
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # El directorio global /static
]

# Verificar que los directorios existen
for static_dir in STATICFILES_DIRS:
    if static_dir.exists():
        print(f"✅ Directorio estático encontrado: {static_dir}")
    else:
        print(f"⚠️  Directorio estático no existe: {static_dir}")

# STATICFILES_FINDERS - Incluye el finder para apps
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',  # Busca en STATICFILES_DIRS
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # Busca en app/static/
]

# Verificar archivos en la app core
core_static_dir = BASE_DIR / 'core' / 'static' / 'core' / 'css'
if core_static_dir.exists():
    css_files = list(core_static_dir.glob('*.css'))
    print(f"✅ CSS files en core/static/core/css/: {[f.name for f in css_files]}")
    if any(f.name == 'variables.css' for f in css_files):
        print("✅ variables.css encontrado en core/static/core/css/")
    else:
        print("❌ variables.css NO encontrado")
else:
    print(f"❌ Directorio core/static/core/css/ no existe: {core_static_dir}")

# Storage - Configuración específica para Railway
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Configuración adicional de WhiteNoise
WHITENOISE_USE_FINDERS = True  # Importante para development/staging
WHITENOISE_AUTOREFRESH = True  # Solo para debugging

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

# Session configuration
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True

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
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print('🚀 Railway production settings loaded successfully')