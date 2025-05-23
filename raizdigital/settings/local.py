from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Cargar variables del archivo .env si existe
def load_env_file():
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        print(f'📁 Cargando .env desde: {env_file}')
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip()
        print('✅ Variables .env cargadas')
    else:
        print(f'⚠️  Archivo .env no encontrado en: {env_file}')

load_env_file()

# Configuración de PostgreSQL Railway
DATABASE_URL = os.environ.get('DATABASE_URL')

print(f'🔍 DATABASE_URL disponible: {"SÍ" if DATABASE_URL else "NO"}')

if DATABASE_URL:
    print('🚀 Conectando a Railway PostgreSQL via DATABASE_URL')
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
        # Añadir configuración SSL para Railway
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }
        print('✅ Configuración con dj_database_url exitosa')
        
        # Mostrar info de conexión (sin contraseña)
        db_config = DATABASES['default']
        print(f'🐘 Conectando a: {db_config["USER"]}@{db_config["HOST"]}:{db_config["PORT"]}/{db_config["NAME"]}')
        
    except ImportError:
        print('❌ dj_database_url no disponible')
        print('💡 Instalar con: pip install dj-database-url')
        
        # Parser manual como fallback
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
                    'OPTIONS': {
                        'sslmode': 'require',
                    },
                }
            }
            print(f'✅ BD configurada manualmente: {user}@{host}:{port}/{database}')
        else:
            print('❌ No se pudo parsear DATABASE_URL')
            print(f'DATABASE_URL format: {DATABASE_URL[:50]}...')
else:
    # Usar variables individuales como fallback
    print('🔄 Usando variables individuales de Railway')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PGDATABASE', 'railway'),
            'USER': os.environ.get('PGUSER', 'postgres'),
            'PASSWORD': os.environ.get('PGPASSWORD', ''),
            'HOST': os.environ.get('PGHOST', 'localhost'),
            'PORT': os.environ.get('PGPORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',  # Importante para Railway
            },
        }
    }
    db_config = DATABASES['default']
    print(f'🐘 Conectando a Railway: {db_config["USER"]}@{db_config["HOST"]}:{db_config["PORT"]}/{db_config["NAME"]}')
    
    # Verificar que tenemos las credenciales mínimas
    required_vars = ['PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f'❌ Variables faltantes: {missing_vars}')
        print('💡 Verifica tu archivo .env')

print('=' * 50)