import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Para desarrollo: usa tu .env
# Para producción: Railway proporcionará la variable SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')

# Si no hay SECRET_KEY en variables de entorno, lanzar error informativo
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY no encontrada. "
        "Para desarrollo local: asegúrate de tener un archivo .env con SECRET_KEY. "
        "Para producción: configura SECRET_KEY en las variables de entorno de Railway."
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = []

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AuthenticationMiddleware',  
    'core.middleware.SessionSecurityMiddleware',  
]




# CONFIGURACIÓN DE SESIONES MÁS SEGURA
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usar base de datos
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_COOKIE_SECURE = True  # Solo HTTPS en producción
SESSION_COOKIE_HTTPONLY = True  # No accesible desde JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF
SESSION_SAVE_EVERY_REQUEST = True  # Actualizar sesión en cada request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Cerrar al cerrar navegador

# CONFIGURACIÓN DE SEGURIDAD ADICIONAL
CSRF_COOKIE_SECURE = True  # Solo HTTPS en producción
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# LOGGING PARA AUDITORÍA
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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core.middleware': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'core.decorators': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}



ROOT_URLCONF = 'raizdigital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'raizdigital.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE', 'raiz_digital'),
        'USER': os.environ.get('PGUSER', 'postgres'),
        'PASSWORD': os.environ.get('PGPASSWORD', ''),
        'HOST': os.environ.get('PGHOST', 'localhost'),
        'PORT': os.environ.get('PGPORT', '5432'),
        'OPTIONS': {
            'sslmode': 'prefer',
        },
        'ATOMIC_REQUESTS': True,
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Verificar si existe la carpeta static antes de agregarla
static_dir = BASE_DIR / "static"
if static_dir.exists():
    STATICFILES_DIRS = [static_dir]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'