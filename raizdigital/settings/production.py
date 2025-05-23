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

# =================================
# CONFIGURACIÓN DE BASE DE DATOS - MEJORADA
# =================================

print("🗄️  Configurando base de datos...")

# Verificar qué variables de BD tenemos disponibles
db_vars = {
    'DATABASE_URL': os.environ.get('DATABASE_URL'),
    'PGHOST': os.environ.get('PGHOST'),
    'PGDATABASE': os.environ.get('PGDATABASE'),
    'PGUSER': os.environ.get('PGUSER'),
    'PGPASSWORD': os.environ.get('PGPASSWORD'),
    'PGPORT': os.environ.get('PGPORT'),
}

print("Variables de BD disponibles:")
for key, value in db_vars.items():
    if value:
        if 'PASSWORD' in key or 'URL' in key:
            print(f"  {key}: {'*' * min(len(str(value)), 10)}")
        else:
            print(f"  {key}: {value}")
    else:
        print(f"  {key}: NO DISPONIBLE")

DATABASES = {}

# Opción 1: Usar DATABASE_URL (preferido)
if db_vars['DATABASE_URL']:
    print("🔗 Usando DATABASE_URL para conexión")
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(db_vars['DATABASE_URL'])}
        
        # Asegurar configuración SSL para Railway
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
            'connect_timeout': 60,
        }
        DATABASES['default']['CONN_MAX_AGE'] = 600
        
        print("✅ Base de datos configurada con dj_database_url")
        
    except ImportError:
        print("⚠️  dj_database_url no disponible, usando parser manual")
        import re
        match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_vars['DATABASE_URL'])
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
                    'OPTIONS': {
                        'sslmode': 'require',
                        'connect_timeout': 60,
                    },
                    'CONN_MAX_AGE': 600,
                }
            }
            print(f"✅ BD configurada manualmente: {user}@{host}:{port}/{database}")
        else:
            print("❌ ERROR: No se pudo parsear DATABASE_URL")
            raise ValueError("DATABASE_URL tiene formato inválido")

# Opción 2: Usar variables individuales
elif all([db_vars['PGHOST'], db_vars['PGUSER'], db_vars['PGPASSWORD'], db_vars['PGDATABASE']]):
    print("🔧 Usando variables de entorno individuales")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_vars['PGDATABASE'],
            'USER': db_vars['PGUSER'],
            'PASSWORD': db_vars['PGPASSWORD'],
            'HOST': db_vars['PGHOST'],
            'PORT': db_vars['PGPORT'] or '5432',
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 60,
            },
            'CONN_MAX_AGE': 600,
        }
    }
    print(f"✅ BD configurada: {db_vars['PGUSER']}@{db_vars['PGHOST']}:{db_vars['PGPORT']}/{db_vars['PGDATABASE']}")

else:
    print("❌ CRITICAL: No se encontraron variables de base de datos")
    print("💡 Verifica que Railway tenga configuradas las variables:")
    print("   - DATABASE_URL (preferido)")
    print("   - O: PGHOST, PGUSER, PGPASSWORD, PGDATABASE, PGPORT")
    sys.exit(1)

# Verificar que tenemos configuración válida
if not DATABASES.get('default'):
    print("❌ CRITICAL: No se pudo configurar la base de datos")
    sys.exit(1)

# Mostrar configuración final (sin contraseña)
final_config = DATABASES['default'].copy()
if 'PASSWORD' in final_config:
    final_config['PASSWORD'] = '***'
print(f"🐘 Configuración final de BD: {final_config}")

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
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS - CORREGIDA
# =================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Crear directorio staticfiles
STATIC_ROOT.mkdir(exist_ok=True)
print(f"📁 STATIC_ROOT: {STATIC_ROOT}")

# STATICFILES_DIRS - Configuración correcta para tu estructura
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # El directorio global /static (si existe)
]

# Solo añadir directorios que existen
existing_dirs = [d for d in STATICFILES_DIRS if d.exists()]
STATICFILES_DIRS = existing_dirs

# Verificar que los directorios existen
for static_dir in STATICFILES_DIRS:
    print(f"✅ Directorio estático encontrado: {static_dir}")

if not STATICFILES_DIRS:
    print("⚠️  No se encontraron directorios estáticos en STATICFILES_DIRS")

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

# Configuración de logging mejorada
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
            'level': 'ERROR',  # Solo errores de BD para no saturar logs
            'propagate': False,
        },
        'django.contrib.staticfiles': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print('🚀 Railway production settings loaded successfully')
print('=' * 60)