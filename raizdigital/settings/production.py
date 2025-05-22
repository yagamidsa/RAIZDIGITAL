from .base import *
import os
import sys

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
]

# Debug completo de variables de entorno
print("=" * 50)
print("DEBUG: Variables de entorno de Railway")
print("=" * 50)

db_vars = ['DATABASE_URL', 'PGDATABASE', 'PGHOST', 'PGUSER', 'PGPASSWORD', 'PGPORT']
for var in db_vars:
    value = os.environ.get(var)
    if value:
        # No mostrar la contraseña completa por seguridad
        if 'PASSWORD' in var:
            print(f"{var}: {'*' * len(value)}")
        else:
            print(f"{var}: {value}")
    else:
        print(f"{var}: NO CONFIGURADA")

print("=" * 50)

# Configuración de base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    print("✅ Usando DATABASE_URL")
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
    except ImportError:
        print("❌ dj_database_url no está instalado")
        sys.exit(1)
elif all([os.environ.get('PGHOST'), os.environ.get('PGDATABASE'), 
          os.environ.get('PGUSER'), os.environ.get('PGPASSWORD')]):
    print("✅ Usando variables PostgreSQL individuales")
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
            'ATOMIC_REQUESTS': True,
        }
    }
else:
    print("❌ FALTA CONFIGURACIÓN DE BASE DE DATOS")
    print("Variables faltantes:")
    for var in ['PGHOST', 'PGDATABASE', 'PGUSER', 'PGPASSWORD']:
        if not os.environ.get(var):
            print(f"  - {var}")
    print("🔧 Ve a Railway y agrega PostgreSQL al proyecto")
    # No hacer sys.exit() para poder ver los logs

# Test de conexión
print("🔍 Intentando conectar a la base de datos...")

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}