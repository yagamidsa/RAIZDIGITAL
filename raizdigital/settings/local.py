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

# Configuración de PostgreSQL local
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
    }
}

print(f'🐘 Conectando a PostgreSQL local: {DATABASES["default"]["USER"]}@{DATABASES["default"]["HOST"]}:{DATABASES["default"]["PORT"]}/{DATABASES["default"]["NAME"]}')
