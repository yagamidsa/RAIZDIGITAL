#!/usr/bin/env python3
"""
Script de migración automática para Railway
Se ejecuta una sola vez al desplegar
"""

import os
import subprocess
import sys

def check_if_data_exists():
    """Verificar si ya hay datos en la BD"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        result = subprocess.run([
            'psql', database_url, '-t', '-c', 
            "SELECT count(*) FROM raiz.usuarios;"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            count = int(result.stdout.strip())
            return count > 0
        return False
    except:
        return False

def migrate_data():
    """Ejecutar migración de datos"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL no encontrada")
        return False
    
    # Verificar si ya hay datos
    if check_if_data_exists():
        print("✅ Los datos ya existen en la base de datos")
        return True
    
    # Verificar archivo de migración
    if not os.path.exists('migrate_data.sql'):
        print("⚠️  Archivo migrate_data.sql no encontrado")
        return False
    
    print("📥 Migrando datos...")
    try:
        result = subprocess.run([
            'psql', database_url, '-f', 'migrate_data.sql', '-q'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Migración de datos completada")
            
            # Verificar migración
            if check_if_data_exists():
                count_result = subprocess.run([
                    'psql', database_url, '-t', '-c', 
                    "SELECT count(*) FROM raiz.usuarios;"
                ], capture_output=True, text=True, timeout=30)
                
                if count_result.returncode == 0:
                    user_count = count_result.stdout.strip()
                    print(f"👥 Usuarios migrados: {user_count}")
            
            return True
        else:
            print(f"❌ Error en migración: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout en migración")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Verificando migración de datos...")
    
    # Crear archivo de marca si la migración es exitosa
    if migrate_data():
        with open('.data_migrated', 'w') as f:
            f.write('migrated')
        print("🎉 Proceso completado")
    else:
        print("❌ Migración falló")
        sys.exit(1)