from .base import *
import os
from pathlib import Path

# Cargar variables del archivo .env para desarrollo local
def load_env_file():
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Solo establecer si no existe ya en el entorno
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip()

# Cargar el archivo .env
load_env_file()

# Configuración para desarrollo
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de datos local (si tienes configuración local diferente)
# Mantener la configuración de base.py o sobrescribir aquí si necesitas