#!/usr/bin/env python
"""Script para actualizar contraseñas en la base de datos PostgreSQL."""
import psycopg2
import sys
import getpass
from django.contrib.auth.hashers import make_password

def conectar_bd():
    """Conecta a la base de datos PostgreSQL."""
    try:
        # Valores predeterminados de settings.py
        dbname = "raiz_digital"
        user = "yagami"
        password = "Ipsos2012*"
        host = "localhost"
        port = "5432"
        
        # Preguntar si usar valores predeterminados
        use_defaults = input("¿Usar valores de conexión predeterminados? (s/n): ").lower() == 's'
        
        if not use_defaults:
            dbname = input(f"Nombre de la base de datos [{dbname}]: ") or dbname
            user = input(f"Usuario [{user}]: ") or user
            password = getpass.getpass(f"Contraseña: ") or password
            host = input(f"Host [{host}]: ") or host
            port = input(f"Puerto [{port}]: ") or port
        
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("✅ Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        sys.exit(1)

def listar_usuarios(conn):
    """Muestra usuarios en la base de datos."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, password, nombre, apellido, email
                FROM raiz.usuarios
                ORDER BY username
            """)
            usuarios = cur.fetchall()
            
            if not usuarios:
                print("No hay usuarios en la base de datos.")
                return []
            else:
                print(f"\n=== USUARIOS EN LA BASE DE DATOS ({len(usuarios)}) ===")
                for i, user in enumerate(usuarios, 1):
                    print(f"{i}. ID: {user[0]}")
                    print(f"   Username: {user[1]}")
                    # Mostrar las primeras 20 caracteres de la contraseña para diagnóstico
                    password_preview = user[2][:20] + "..." if user[2] and len(user[2]) > 20 else user[2]
                    print(f"   Contraseña (hash): {password_preview}")
                    print(f"   Nombre: {user[3]} {user[4]}")
                    print(f"   Email: {user[5]}")
                    print("-" * 40)
                return usuarios
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        return []

def actualizar_contrasena(conn, usuarios):
    """Actualiza la contraseña de un usuario específico."""
    if not usuarios:
        print("No hay usuarios para actualizar contraseñas.")
        return
    
    try:
        # Seleccionar un usuario
        user_index = int(input("Seleccione el número del usuario para actualizar la contraseña: ")) - 1
        if user_index < 0 or user_index >= len(usuarios):
            print("Número de usuario inválido.")
            return
        
        user_id = usuarios[user_index][0]
        username = usuarios[user_index][1]
        
        # Obtener y hashear la nueva contraseña
        nueva_contrasena = getpass.getpass("Nueva contraseña: ")
        confirmar_contrasena = getpass.getpass("Confirmar contraseña: ")
        
        if nueva_contrasena != confirmar_contrasena:
            print("❌ Las contraseñas no coinciden.")
            return
        
        # Hashear la contraseña y actualizarla en la base de datos
        hashed_password = make_password(nueva_contrasena)
        
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE raiz.usuarios SET password = %s WHERE id = %s",
                (hashed_password, user_id)
            )
            conn.commit()
            
            print(f"✅ Contraseña actualizada para el usuario '{username}'")
            print(f"   Nueva contraseña (hasheada): {hashed_password[:20]}...")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al actualizar la contraseña: {e}")

def detectar_problemas_contrasena(conn):
    """Detecta usuarios con posibles problemas de contraseña no hasheada."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, password FROM raiz.usuarios")
            usuarios = cur.fetchall()
            
            problemas = []
            for user in usuarios:
                user_id, username, password = user
                
                # Detectar si la contraseña no está hasheada
                is_hashed = (
                    password and
                    len(password) > 30 and
                    (password.startswith('pbkdf2_sha256$') or 
                     password.startswith('bcrypt$') or 
                     password.startswith('argon2'))
                )
                
                if not is_hashed:
                    problemas.append((user_id, username, password))
            
            if problemas:
                print(f"\n⚠️ DETECTADOS {len(problemas)} USUARIOS CON POSIBLES PROBLEMAS DE CONTRASEÑA:")
                for user_id, username, password in problemas:
                    print(f"- {username} (ID: {user_id})")
                    print(f"  Contraseña actual: {password}")
                    print("  Problema: La contraseña no parece estar hasheada correctamente")
                    print("-" * 40)
                    
                return problemas
            else:
                print("✅ No se detectaron problemas de contraseña.")
                return []
    except Exception as e:
        print(f"❌ Error al detectar problemas de contraseña: {e}")
        return []

def arreglar_todas_contrasenas(conn, problemas):
    """Arregla todas las contraseñas problemáticas."""
    if not problemas:
        print("No hay contraseñas problemáticas para arreglar.")
        return
    
    try:
        for user_id, username, password_actual in problemas:
            print(f"\nActualizando contraseña para {username}:")
            print(f"Contraseña actual (no hasheada): {password_actual}")
            
            # Usar la contraseña actual como base para la nueva contraseña hasheada
            nueva_contrasena = password_actual or "password123"  # Default si es None
            hashed_password = make_password(nueva_contrasena)
            
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE raiz.usuarios SET password = %s WHERE id = %s",
                    (hashed_password, user_id)
                )
            
            print(f"✅ Contraseña actualizada para {username}")
            print(f"Nueva contraseña (texto plano): {nueva_contrasena}")
            print(f"Contraseña hasheada: {hashed_password[:20]}...")
            print("-" * 40)
        
        conn.commit()
        print("\n✅ Todas las contraseñas problemáticas han sido actualizadas.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al arreglar contraseñas: {e}")

def probar_login(conn):
    """Prueba el login para un usuario específico."""
    try:
        username = input("Username para probar: ")
        password = getpass.getpass("Contraseña: ")
        
        # Buscar usuario
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, password, nombre, apellido FROM raiz.usuarios WHERE username = %s",
                (username,)
            )
            user_data = cur.fetchone()
            
            if not user_data:
                print(f"❌ Usuario '{username}' no encontrado en la base de datos.")
                return
            
            user_id, db_username, db_password, nombre, apellido = user_data
            
            # Verificar contraseña
            from django.contrib.auth.hashers import check_password
            password_valid = check_password(password, db_password)
            
            if password_valid:
                print(f"✅ Login exitoso para '{username}'!")
                print(f"Nombre: {nombre} {apellido}")
                print(f"ID: {user_id}")
            else:
                print(f"❌ Contraseña incorrecta para '{username}'")
                print(f"Contraseña ingresada: {password}")
                print(f"Hash almacenado: {db_password[:20]}...")
    except Exception as e:
        print(f"❌ Error al probar login: {e}")

def main():
    print("\n===== GESTOR DE CONTRASEÑAS PARA RAÍZ DIGITAL =====")
    print("Este script te permite gestionar las contraseñas de usuarios.")
    
    # Importar Django y configurarlo
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raizdigital.settings')
    django.setup()
    
    conn = conectar_bd()
    
    try:
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Listar todos los usuarios")
            print("2. Actualizar contraseña de un usuario específico")
            print("3. Detectar problemas de contraseña no hasheada")
            print("4. Arreglar automáticamente todas las contraseñas problemáticas")
            print("5. Probar login con un usuario")
            print("0. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                listar_usuarios(conn)
            elif opcion == "2":
                usuarios = listar_usuarios(conn)
                actualizar_contrasena(conn, usuarios)
            elif opcion == "3":
                problemas = detectar_problemas_contrasena(conn)
                if problemas:
                    respuesta = input("\n¿Desea arreglar automáticamente estas contraseñas? (s/n): ")
                    if respuesta.lower() == 's':
                        arreglar_todas_contrasenas(conn, problemas)
            elif opcion == "4":
                problemas = detectar_problemas_contrasena(conn)
                arreglar_todas_contrasenas(conn, problemas)
            elif opcion == "5":
                probar_login(conn)
            elif opcion == "0":
                print("Saliendo...")
                break
            else:
                print("Opción no válida, intente nuevamente.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()