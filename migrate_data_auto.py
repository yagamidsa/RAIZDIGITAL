#!/usr/bin/env python
"""Script específico para migrar productos arreglando el problema de fecha_actualizacion."""
import psycopg2
import sys
from datetime import datetime

def conectar_local():
    """Conecta a la base de datos PostgreSQL local."""
    try:
        conn = psycopg2.connect(
            dbname="raiz_digital",
            user="yagami",
            password="Ipsos2012*",
            host="localhost",
            port="5432"
        )
        print("✅ Conexión exitosa a la base de datos local")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos local: {e}")
        return None

def conectar_railway():
    """Conecta a Railway."""
    try:
        railway_url = "postgresql://postgres:ssmLfCJxPOHMssJAjxDHrCgOkPIZwvqn@switchyard.proxy.rlwy.net:48272/railway"
        conn = psycopg2.connect(railway_url)
        print("✅ Conexión exitosa a Railway")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar a Railway: {e}")
        return None

def migrar_productos():
    """Migra productos arreglando el problema de fecha_actualizacion NULL."""
    
    conn_local = conectar_local()
    if not conn_local:
        return False
    
    conn_railway = conectar_railway()
    if not conn_railway:
        return False
    
    try:
        # Obtener productos de local
        with conn_local.cursor() as cur_local:
            cur_local.execute("SELECT * FROM raiz.productos")
            productos = cur_local.fetchall()
            columnas = [desc[0] for desc in cur_local.description]
            
        print(f"📦 Encontrados {len(productos)} productos en local")
        
        # Obtener estructura de Railway
        with conn_railway.cursor() as cur_railway:
            cur_railway.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'raiz' AND table_name = 'productos'
                ORDER BY ordinal_position
            """)
            columnas_railway = [row[0] for row in cur_railway.fetchall()]
            
        print(f"📋 Columnas en Railway: {columnas_railway}")
        print(f"📋 Columnas en local: {columnas}")
        
        # Limpiar tabla productos en Railway
        with conn_railway.cursor() as cur_railway:
            cur_railway.execute("TRUNCATE TABLE raiz.productos RESTART IDENTITY CASCADE")
            print("🧹 Tabla productos limpiada")
            
            # Preparar mapeo de columnas
            mapeo = {}
            for i, col_local in enumerate(columnas):
                if col_local in columnas_railway:
                    mapeo[col_local] = i
            
            print(f"📝 Columnas a migrar: {list(mapeo.keys())}")
            
            # Migrar producto por producto
            productos_migrados = 0
            
            for producto in productos:
                try:
                    # Preparar datos del producto
                    datos_producto = {}
                    for col_railway in columnas_railway:
                        if col_railway in mapeo:
                            valor = producto[mapeo[col_railway]]
                            
                            # Arreglar fecha_actualizacion si es NULL
                            if col_railway == 'fecha_actualizacion' and valor is None:
                                # Usar fecha_creacion si existe, sino usar NOW()
                                if 'fecha_creacion' in mapeo:
                                    valor = producto[mapeo['fecha_creacion']]
                                else:
                                    valor = datetime.now()
                            
                            datos_producto[col_railway] = valor
                    
                    # Construir INSERT
                    columnas_insert = list(datos_producto.keys())
                    valores_insert = list(datos_producto.values())
                    
                    columnas_str = ', '.join(columnas_insert)
                    placeholders = ', '.join(['%s'] * len(valores_insert))
                    
                    query = f"INSERT INTO raiz.productos ({columnas_str}) VALUES ({placeholders})"
                    
                    # Ejecutar INSERT
                    cur_railway.execute(query, valores_insert)
                    conn_railway.commit()
                    productos_migrados += 1
                    
                    print(f"  ✅ Producto migrado: {datos_producto.get('nombre', 'Sin nombre')}")
                    
                except Exception as e:
                    conn_railway.rollback()
                    print(f"  ❌ Error migrando producto: {e}")
                    print(f"     Datos: {datos_producto}")
            
            print(f"\n📊 Productos migrados: {productos_migrados}/{len(productos)}")
            
            # Verificar migración
            cur_railway.execute("SELECT COUNT(*) FROM raiz.productos")
            count = cur_railway.fetchone()[0]
            print(f"✅ Total productos en Railway: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
    finally:
        conn_local.close()
        conn_railway.close()

if __name__ == "__main__":
    print("===== MIGRACIÓN ESPECÍFICA DE PRODUCTOS =====")
    if migrar_productos():
        print("🎉 ¡Migración de productos completada!")
    else:
        print("❌ La migración de productos falló")