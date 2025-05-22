import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-railway-fallback-key-12345')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
    '*',  # Temporalmente permitir todos los hosts
]

# Application definition
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

# Debug de variables de entorno
print("🔍 RAILWAY DEBUG - Variables de entorno:")
print("-" * 50)

env_vars = [
    'DATABASE_URL', 'PGDATABASE', 'PGHOST', 'PGUSER', 'PGPASSWORD', 'PGPORT',
    'SECRET_KEY', 'DEBUG', 'DJANGO_SETTINGS_MODULE', 'PORT'
]

for var in env_vars:
    value = os.environ.get(var)
    if value:
        if 'PASSWORD' in var or 'SECRET' in var:
            print(f"✅ {var}: {'*' * min(len(value), 20)}")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: NO CONFIGURADA")

print("-" * 50)

# Configuración de base de datos con múltiples fallbacks
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    print("🎯 Usando DATABASE_URL de Railway")
    # Parsear DATABASE_URL manualmente si dj_database_url no está disponible
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
        print("✅ dj_database_url parseado correctamente")
    except ImportError:
        print("⚠️ dj_database_url no disponible, parseando manualmente")
        # Parseo manual básico de DATABASE_URL
        # Formato: postgres://user:password@host:port/database
        if DATABASE_URL.startswith('postgres://'):
            url_parts = DATABASE_URL.replace('postgres://', '').split('/')
            if len(url_parts) >= 2:
                auth_host = url_parts[0]
                database = url_parts[1]
                
                if '@' in auth_host:
                    auth, host_port = auth_host.split('@')
                    if ':' in auth:
                        user, password = auth.split(':', 1)
                    else:
                        user, password = auth, ''
                    
                    if ':' in host_port:
                        host, port = host_port.split(':')
                    else:
                        host, port = host_port, '5432'
                    
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
                            },
                            'CONN_MAX_AGE': 600,
                        }
                    }
                    print(f"✅ Base de datos parseada: {user}@{host}:{port}/{database}")
                else:
                    print("❌ No se pudo parsear DATABASE_URL")
                    DATABASES = {}
            else:
                print("❌ Formato de DATABASE_URL inválido")
                DATABASES = {}

elif all([os.environ.get('PGHOST'), os.environ.get('PGDATABASE'), 
          os.environ.get('PGUSER'), os.environ.get('PGPASSWORD')]):
    print("🎯 Usando variables PostgreSQL individuales")
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
        }
    }
    print(f"✅ Configuración individual: {os.environ.get('PGUSER')}@{os.environ.get('PGHOST')}")
else:
    print("❌ NO HAY CONFIGURACIÓN DE BASE DE DATOS")
    print("🔧 SOLUCIÓN: Agrega PostgreSQL en Railway Dashboard")
    print("   1. Ve a tu proyecto en Railway")
    print("   2. Click 'New' → 'Database' → 'Add PostgreSQL'")
    print("   3. Espera a que se configure")
    
    # Base de datos sqlite temporal para que no falle completamente
    print("⚠️ Usando SQLite temporal para evitar crash")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Verificar si existe la carpeta static
if os.path.exists(os.path.join(BASE_DIR, 'static')):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Whitenoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

print("🚀 Configuración de Django completada")
print("=" * 50)