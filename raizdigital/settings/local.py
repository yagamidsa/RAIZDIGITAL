from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Cargar variables del archivo .env si existe
def load_env_file():
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip()

load_env_file()

# Configuración de PostgreSQL local COMPATIBLE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'raiz_digital'),
        'USER': os.environ.get('DB_USER', 'yagami'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'Ipsos2012*'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'prefer',
        },
        # IMPORTANTE: Transacciones manuales en local para compatibilidad
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 0,  # Sin pooling en local para evitar problemas
    }
}

# MIDDLEWARE COMPATIBLE (incluir el personalizado si existe)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Intentar añadir middleware personalizado si existe
try:
    import core.middleware
    MIDDLEWARE.append('core.middleware.AuthenticationMiddleware')
    print("✅ Middleware personalizado añadido")
except ImportError:
    print("⚠️ Middleware personalizado no encontrado, usando solo middlewares estándar")

print(f'🐘 Conectando a PostgreSQL local: {DATABASES["default"]["USER"]}@{DATABASES["default"]["HOST"]}:{DATABASES["default"]["PORT"]}/{DATABASES["default"]["NAME"]}')
print(f'🔧 ATOMIC_REQUESTS: {DATABASES["default"]["ATOMIC_REQUESTS"]}')
print(f'🔧 DEBUG: {DEBUG}')