from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import re
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.db import connection, transaction
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import uuid
import datetime
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
import os
from django.core.files.storage import FileSystemStorage
from .models import *
import datetime
import logging

logger = logging.getLogger(__name__)

# Importar decoradores personalizados (SI EXISTEN)
try:
    from .decorators import login_required_custom, admin_required, ajax_login_required, session_refresh, get_user_info
    DECORATORS_AVAILABLE = True
except ImportError:
    # Si no existen los decoradores, crearlos aquí mismo
    DECORATORS_AVAILABLE = False

logger = logging.getLogger(__name__)

def index(request):
    """Página de inicio - pública"""
    return render(request, 'core/index.html')



def login_view(request):
    """Vista de login mejorada con manejo de mensajes de logout"""
    
    # Si ya está logueado, redirigir al marketplace
    if request.session.get('user_id'):
        return redirect('core:marketplace')
    
    # NUEVO: Mostrar mensaje de logout solo si viene directamente de logout
    logout_message = None
    referer = request.META.get('HTTP_REFERER', '')
    if '/logout/' in referer:
        logout_message = "Sesión cerrada correctamente."
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        logger.info(f"Intento de login: {username} desde IP {request.META.get('REMOTE_ADDR')}")
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT u.id, u.username, u.password, u.nombre, u.apellido, 
                           c.id as comunidad_id, c.nombre as comunidad_nombre, u.activo
                    FROM raiz.usuarios u
                    LEFT JOIN raiz.comunidades c ON u.id_comunidad = c.id
                    WHERE u.username = %s
                """, [username])
                user_data = cursor.fetchone()
            
            if user_data:
                user_id, db_username, db_password, nombre, apellido, comunidad_id, comunidad_nombre, activo = user_data
                
                # Verificar que el usuario esté activo
                if not activo:
                    logger.warning(f"Intento de login con usuario inactivo: {username}")
                    return render(request, 'core/login.html', {
                        'error': 'Tu cuenta está desactivada. Contacta al administrador.',
                        'username': username,
                        'logout_message': logout_message
                    })
                
                # Verificar contraseña
                password_valid = check_password(password, db_password)
                
                if password_valid:
                    # LIMPIAR SESIÓN ANTERIOR
                    request.session.flush()
                    
                    # CREAR NUEVA SESIÓN SEGURA
                    request.session['user_id'] = str(user_id)
                    request.session['username'] = db_username
                    request.session['nombre'] = nombre
                    request.session['apellido'] = apellido
                    
                    if comunidad_id:
                        request.session['comunidad_id'] = comunidad_id
                        request.session['comunidad_nombre'] = comunidad_nombre
                    
                    # Configurar sesión
                    request.session.set_expiry(3600)  # 1 hora
                    request.session['last_activity'] = datetime.datetime.now().timestamp()
                    request.session['login_ip'] = request.META.get('REMOTE_ADDR', '')
                    
                    # Actualizar último login en BD
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE raiz.usuarios SET ultimo_login = %s WHERE id = %s",
                            [datetime.datetime.now(), user_id]
                        )
                    
                    logger.info(f"Login exitoso: {username} (ID: {user_id})")
                    return redirect('core:marketplace')
                else:
                    logger.warning(f"Contraseña incorrecta para usuario: {username}")
                    return render(request, 'core/login.html', {
                        'error': 'Contraseña incorrecta',
                        'username': username,
                        'logout_message': logout_message
                    })
            else:
                logger.warning(f"Usuario no encontrado: {username}")
                return render(request, 'core/login.html', {
                    'error': 'Usuario no encontrado',
                    'username': username,
                    'logout_message': logout_message
                })
                
        except Exception as e:
            logger.error(f"Error en login: {e}")
            return render(request, 'core/login.html', {
                'error': 'Error en el sistema. Intenta más tarde.',
                'username': username,
                'logout_message': logout_message
            })
    
    # GET request - mostrar formulario con mensaje de logout si corresponde
    return render(request, 'core/login.html', {
        'logout_message': logout_message
    })


def password_recovery(request):
    """Vista de recuperación de contraseña - pública"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = Usuario.objects.get(email=email)
            recovery_token = str(uuid.uuid4())
            user.token_recuperacion = recovery_token
            user.fecha_token = datetime.datetime.now()
            user.save(update_fields=['token_recuperacion', 'fecha_token'])
            
            context = {
                'success': 'Se han enviado instrucciones para restablecer tu contraseña.'
            }
            return render(request, 'core/password_recovery.html', context)
            
        except Usuario.DoesNotExist:
            context = {
                'success': 'Si el correo está registrado, recibirás instrucciones.'
            }
            return render(request, 'core/password_recovery.html', context)
    
    return render(request, 'core/password_recovery.html')


#@login_required
#def marketplace(request):
#    return render(request, 'core/marketplace.html')

# VISTAS PROTEGIDAS (requieren autenticación)
@login_required_custom
@session_refresh
def marketplace(request):
    """Vista del marketplace - PROTEGIDA"""
    user_info = get_user_info(request)
    
    context = {
        'username': user_info['username'],
        'nombre': user_info['nombre'],
        'apellido': user_info['apellido'],
        'nombre_completo': f"{user_info['nombre']} {user_info['apellido']}".strip(),
        'community_name': user_info['comunidad_nombre']
    }
    
    return render(request, 'core/marketplace_home.html', context)


@login_required_custom
@session_refresh
def noticias(request):
    """Vista de noticias - PROTEGIDA"""
    user_info = get_user_info(request)
    """
    Vista para mostrar el listado de noticias.
    Versión optimizada para solucionar problemas con el filtrado de comunidad.
    """
    # Obtener parámetros de la URL
    query = request.GET.get('q', '')
    page = request.GET.get('page', '1')  # Aseguramos que sea string inicialmente
    
    # Convertir página a entero de forma segura
    try:
        page_number = int(page)
    except (ValueError, TypeError):
        page_number = 1
    
    # Verificar si el usuario está logueado
    is_logged_in = 'user_id' in request.session
    
    # Variables para tracking de comunidad
    user_comunidad_id = None
    user_comunidad_nombre = None
    filter_by_community = False
    
    # DEBUG: Imprimir información de la sesión
    print("Variables de sesión:")
    for key, value in request.session.items():
        print(f"- {key}: {value}")
    
    # Obtener información de la comunidad del usuario si está logueado
    if is_logged_in:
        # Obtener ID de comunidad y asegurar que sea entero (algunos sistemas lo guardan como string)
        user_comunidad_id_raw = request.session.get('comunidad_id')
        if user_comunidad_id_raw is not None:
            try:
                # Intentar convertir a entero si es string
                user_comunidad_id = int(user_comunidad_id_raw)
            except (ValueError, TypeError):
                # Si falla, mantener el valor original
                user_comunidad_id = user_comunidad_id_raw
        
        user_comunidad_nombre = request.session.get('comunidad_nombre')
        filter_by_community = user_comunidad_id is not None
        
        print(f"Usuario logueado: {request.session.get('nombre')} {request.session.get('apellido')}")
        print(f"Comunidad: ID={user_comunidad_id} (tipo: {type(user_comunidad_id)}), Nombre={user_comunidad_nombre}")
    
    # SOLUCIÓN DIRECTA: Obtener todas las noticias manualmente usando SQL
    from django.db import connection
    
    print("\n=== CONSULTA DIRECTA SQL PARA VERIFICAR NOTICIAS ===")
    all_news = []
    
    # 1. Primero obtenemos todas las noticias publicadas
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT n.id, n.titulo, n.resumen, n.contenido, n.slug, n.fecha_publicacion, 
                   n.estado, n.imagen_portada, n.destacado, n.id_comunidad, c.nombre as comunidad_nombre,
                   u.id as autor_id, u.nombre as autor_nombre, u.apellido as autor_apellido
            FROM raiz.noticias n
            LEFT JOIN raiz.comunidades c ON n.id_comunidad = c.id
            LEFT JOIN raiz.usuarios u ON n.id_autor = u.id
            WHERE n.estado = 'publicado'
            ORDER BY n.fecha_publicacion DESC
        """)
        all_news_raw = cursor.fetchall()
        
        print(f"Total noticias encontradas: {len(all_news_raw)}")
        for i, news in enumerate(all_news_raw):
            print(f"Noticia {i+1}: ID={news[0]}, Título='{news[1]}', Comunidad ID={news[9]}, Comunidad Nombre={news[10]}")
            
            # Convertir resultados SQL a objetos Python para la plantilla
            news_obj = {
                'id': news[0], 
                'titulo': news[1],
                'resumen': news[2],
                'contenido': news[3],
                'slug': news[4],
                'fecha_publicacion': news[5],
                'estado': news[6],
                'imagen_portada': news[7] or 'default.jpg',
                'destacado': news[8],
                'id_comunidad_id': news[9],  # Este es el ID de la comunidad
                'id_comunidad': {'id': news[9], 'nombre': news[10]},  # Objeto comunidad simulado
                'id_autor': news[11],
                'autor_nombre': news[12] or 'Usuario',
                'autor_apellido': news[13] or 'Desconocido'
            }
            all_news.append(news_obj)
    
    print("\n=== APLICANDO FILTROS DE COMUNIDAD ===")
    # 2. Si el usuario está logueado y tiene comunidad, filtrar noticias
    filtered_news = []
    
    if filter_by_community:
        print(f"Filtrando por comunidad ID={user_comunidad_id}")
        
        for news in all_news:
            # Verificar si la noticia pertenece a la comunidad del usuario o es global
            if news['id_comunidad_id'] == user_comunidad_id or news['id_comunidad_id'] is None:
                filtered_news.append(news)
                print(f"- Añadiendo noticia '{news['titulo']}' - ID Comunidad: {news['id_comunidad_id']}")
        
        print(f"Total noticias después de filtrar: {len(filtered_news)}")
    else:
        # Si no hay filtro de comunidad, usar todas las noticias
        filtered_news = all_news
        print("No se aplica filtro de comunidad, usando todas las noticias")
    
    # 3. Aplicar filtro de búsqueda si existe
    if query:
        search_results = []
        for news in filtered_news:
            if (query.lower() in news['titulo'].lower() or 
                query.lower() in news['resumen'].lower() or 
                query.lower() in news['contenido'].lower()):
                search_results.append(news)
        filtered_news = search_results
    
    # Configurar paginación manual
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(filtered_news, 4)  # 4 noticias por página
    page = request.GET.get('page', 1)

    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        noticias = paginator.page(1)
    except EmptyPage:
        noticias = paginator.page(paginator.num_pages)
    

    admin_status = is_admin(request)
    request.session['is_admin'] = admin_status

    # 5. Preparar contexto
    context = {
        'noticias': noticias,
        'query': query,
        'current_page': page_number,
        'total_pages': paginator.num_pages,
        'user_comunidad': user_comunidad_nombre,
        'is_admin': admin_status,
        'debug_info': {
            'total_noticias': len(filtered_news),
            'noticias_en_pagina': len(noticias),
            'comunidad_id': user_comunidad_id,
            'comunidad_nombre': user_comunidad_nombre,
            'esta_logueado': is_logged_in,
            'filtro_comunidad_aplicado': filter_by_community,
            'tipo_comunidad_id_sesion': str(type(user_comunidad_id)),
            'tipo_id_comunidad_filtro': 'int (forzado)'
        }
    }
    
    return render(request, 'core/news.html', context)

@login_required_custom
@session_refresh
def noticia_detalle(request, slug):
    """Vista de detalle de noticia - PROTEGIDA"""
    user_info = get_user_info(request)
    """
    Vista mejorada para mostrar el detalle de una noticia con contador de vistas único.
    """
    print(f"\n=== DETALLE DE NOTICIA SOLICITADO ===")
    print(f"Slug recibido: {slug}")
    
    # Verificar que el slug sea válido
    if not slug:
        print("Error: Slug vacío")
        return redirect('core:noticias')
    
    try:
        # Identificar al usuario (desde la sesión o por IP si no está logueado)
        user_id = request.session.get('user_id')
        if not user_id:
            # Si no está logueado, usar la IP como identificador
            user_id = request.META.get('REMOTE_ADDR', 'anonymous')
        
        print(f"Usuario que ve la noticia: {user_id}")
        
        # Variables para controlar el estado de visualización y me gusta
        vista_contabilizada = False
        usuario_dio_like = False
        
        # Obtener la noticia usando SQL directo para mayor control
        from django.db import connection
        with connection.cursor() as cursor:
            # Consulta SQL básica para obtener la noticia
            sql_query = """
                SELECT n.id, n.titulo, n.resumen, n.contenido, n.slug, n.fecha_publicacion, 
                       n.estado, n.imagen_portada, n.destacado, n.id_comunidad, c.nombre as comunidad_nombre,
                       u.id as autor_id, u.nombre as autor_nombre, u.apellido as autor_apellido,
                       n.vistas
                FROM raiz.noticias n
                LEFT JOIN raiz.comunidades c ON n.id_comunidad = c.id
                LEFT JOIN raiz.usuarios u ON n.id_autor = u.id
                WHERE n.slug = %s
            """
            
            # Añadir filtro de estado solo para no-admins
            is_admin = request.session.get('is_admin', False)
            if not is_admin:
                sql_query += " AND n.estado = 'publicado'"
                
            print(f"Ejecutando consulta SQL: {sql_query}")
            cursor.execute(sql_query, [slug])
            noticia_data = cursor.fetchone()
            
            if not noticia_data:
                print(f"Error: No se encontró noticia con slug '{slug}'")
                return redirect('core:noticias')
            
            # Obtener el ID de la noticia para registrar la vista
            noticia_id = noticia_data[0]
            
            # Mapeo de datos de la consulta a un diccionario
            noticia = {
                'id': noticia_id,
                'titulo': noticia_data[1],
                'resumen': noticia_data[2],
                'contenido': noticia_data[3],
                'slug': noticia_data[4],
                'fecha_publicacion': noticia_data[5],
                'estado': noticia_data[6],
                'imagen_portada': noticia_data[7] or 'default.jpg',
                'destacado': noticia_data[8],
                'id_comunidad': noticia_data[9],
                'comunidad_nombre': noticia_data[10],
                'autor_id': noticia_data[11],
                'autor_nombre': noticia_data[12] or 'Usuario',
                'autor_apellido': noticia_data[13] or 'Desconocido',
                'vistas': noticia_data[14] or 0
            }
            
            print(f"Noticia encontrada: {noticia['titulo']} (ID: {noticia['id']})")
            
            # Comprobar si el usuario ya vio esta noticia
            cursor.execute("""
                SELECT id FROM raiz.noticia_vistas 
                WHERE id_noticia = %s AND id_usuario = %s
            """, [str(noticia_id), str(user_id)])
            
            vista_existente = cursor.fetchone()
            
            # Si no existe una vista previa, registrar la nueva vista
            if not vista_existente:
                try:
                    print(f"Registrando nueva vista para noticia {noticia_id} por usuario {user_id}")
                    cursor.execute("""
                        INSERT INTO raiz.noticia_vistas (id_noticia, id_usuario)
                        VALUES (%s, %s)
                    """, [str(noticia_id), str(user_id)])
                    
                    # Incrementar contador de vistas en la tabla de noticias
                    cursor.execute("""
                        UPDATE raiz.noticias 
                        SET vistas = vistas + 1 
                        WHERE id = %s
                    """, [noticia_id])
                    
                    # Actualizar el contador en el objeto noticia que pasamos a la plantilla
                    noticia['vistas'] += 1
                    vista_contabilizada = True
                    
                    print(f"Vista registrada y contador incrementado a {noticia['vistas']}")
                except Exception as e:
                    print(f"Error al registrar vista: {e}")
            else:
                print(f"El usuario ya había visto esta noticia anteriormente")
            
            # Verificar si el usuario ya dio like a esta noticia
            # Primero verificar si la tabla existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'raiz' 
                    AND table_name = 'noticia_likes'
                )
            """)
            
            likes_table_exists = cursor.fetchone()[0]
            
            # Si la tabla no existe, crearla
            if not likes_table_exists:
                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS raiz.noticia_likes (
                            id SERIAL PRIMARY KEY,
                            id_noticia UUID NOT NULL,
                            id_usuario VARCHAR(255) NOT NULL,
                            fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            CONSTRAINT unique_noticia_usuario UNIQUE(id_noticia, id_usuario)
                        )
                    """)
                    print("Tabla de likes creada")
                except Exception as e:
                    print(f"Error al crear tabla de likes: {e}")
            
            # Verificar si el usuario dio like
            cursor.execute("""
                SELECT id FROM raiz.noticia_likes 
                WHERE id_noticia = %s AND id_usuario = %s
            """, [str(noticia_id), str(user_id)])
            
            like_existente = cursor.fetchone()
            usuario_dio_like = like_existente is not None
            
            # Obtener la cantidad de likes
            cursor.execute("""
                SELECT COUNT(*) FROM raiz.noticia_likes 
                WHERE id_noticia = %s
            """, [str(noticia_id)])
            
            cantidad_likes = cursor.fetchone()[0]
        
        # Obtener noticias relacionadas (solo de la comunidad del usuario)
        user_comunidad_id = request.session.get('comunidad_id')
        
        # Asegurar que el ID de comunidad sea entero
        if user_comunidad_id:
            try:
                user_comunidad_id = int(user_comunidad_id)
            except (ValueError, TypeError):
                print(f"Error al convertir ID de comunidad: {user_comunidad_id}")
        
        noticias_relacionadas = []
        with connection.cursor() as cursor:
            # Definir consulta base para noticias relacionadas
            related_sql = """
                SELECT n.id, n.titulo, n.resumen, n.slug, n.fecha_publicacion, n.imagen_portada
                FROM raiz.noticias n
                WHERE n.id != %s
                AND n.estado = 'publicado'
            """
            
            # Filtrar por comunidad - solo usar la comunidad del usuario logueado
            if user_comunidad_id:
                related_sql += " AND n.id_comunidad = %s"
                params = [noticia['id'], user_comunidad_id]
                print(f"Filtrando noticias relacionadas por comunidad: {user_comunidad_id}")
            else:
                # Si no hay comunidad, mostrar noticias globales (sin comunidad)
                related_sql += " AND n.id_comunidad IS NULL"
                params = [noticia['id']]
                print("Filtrando noticias relacionadas globales (sin comunidad)")
            
            related_sql += " ORDER BY n.fecha_publicacion DESC LIMIT 3"
            
            cursor.execute(related_sql, params)
            
            for row in cursor.fetchall():
                noticias_relacionadas.append({
                    'id': row[0],
                    'titulo': row[1],
                    'resumen': row[2],
                    'slug': row[3],
                    'fecha_publicacion': row[4],
                    'imagen_portada': row[5] or 'default.jpg'
                })
        
        # Preparar datos para la plantilla
        context = {
            'noticia': noticia,
            'autor': {
                'nombre': f"{noticia['autor_nombre']} {noticia['autor_apellido']}",
                'id': noticia['autor_id']
            },
            'noticias_relacionadas': noticias_relacionadas,
            'is_admin': is_admin,
            'user_comunidad_id': user_comunidad_id,
            'user_comunidad_nombre': request.session.get('comunidad_nombre', 'Sin comunidad'),
            'vista_contabilizada': vista_contabilizada,
            'usuario_dio_like': usuario_dio_like,
            'cantidad_likes': cantidad_likes,
            'user_id': user_id
        }
        
        print("Renderizando plantilla detail_news.html con éxito")
        return render(request, 'core/detail_news.html', context)
        
    except Exception as e:
        # Log del error y redirección al listado
        print(f"Error al mostrar noticia {slug}: {e}")
        import traceback
        traceback.print_exc()
        return redirect('core:noticias')
    

    

def is_admin(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return False
    """
    Determina si el usuario actual es administrador basado en sus roles.
    """
    print("\n=== VERIFICACIÓN DE ADMIN INICIADA ===")
    print(f"Sesión actual: {dict(request.session)}")
    
    if 'user_id' not in request.session:
        print("❌ No hay user_id en la sesión")
        return False
    
    try:
        user_id = request.session.get('user_id')
        print(f"🔍 Verificando si el usuario {user_id} es administrador")
        
        # Para desarrollo, verifiquemos primero qué usuarios existen
        from django.db import connection
        with connection.cursor() as cursor:
            # Imprimir todas las tablas de usuarios y roles para depuración
            print("Verificando tablas y roles...")
            
            # 1. Verificar si la tabla usuarios_roles existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'raiz' 
                    AND table_name = 'usuarios_roles'
                )
            """)
            table_exists = cursor.fetchone()[0]
            print(f"¿Existe la tabla usuarios_roles? {table_exists}")
            
            # 2. Si existe, verificar roles disponibles
            if table_exists:
                cursor.execute("SELECT id, nombre FROM raiz.roles")
                roles = cursor.fetchall()
                print(f"Roles disponibles: {roles}")
                
                # 3. Verificar asignaciones de roles
                cursor.execute("""
                    SELECT ur.id_usuario, r.nombre 
                    FROM raiz.usuarios_roles ur
                    JOIN raiz.roles r ON ur.id_rol = r.id
                """)
                role_assignments = cursor.fetchall()
                print(f"Asignaciones de roles: {role_assignments}")
                
                # 4. Verificar si el usuario actual tiene rol de admin
                cursor.execute("""
                    SELECT COUNT(*) FROM raiz.usuarios_roles ur
                    JOIN raiz.roles r ON ur.id_rol = r.id
                    WHERE ur.id_usuario = %s 
                    AND r.nombre ILIKE %s
                """, [user_id, '%admin%'])  # Búsqueda más flexible
                
                count = cursor.fetchone()[0]
                is_admin_user = count > 0
                print(f"✅ Usuario {user_id} es admin: {is_admin_user} (conteo: {count})")
                
                # 5. Actualizar sesión
                request.session['is_admin'] = is_admin_user
                request.session.modified = True
                
                return is_admin_user
            else:
                print("⚠️ La tabla usuarios_roles no existe, usando método alternativo")
                # Si las tablas no existen, usa una solución alternativa
                is_admin_user = True  # Para desarrollo
                request.session['is_admin'] = is_admin_user
                request.session.modified = True
                return is_admin_user
                
    except Exception as e:
        print(f"❌ Error verificando rol de administrador: {e}")
        import traceback
        traceback.print_exc()
        
        # Si hay un error, establecer un valor de fallback
        is_admin_user = True  # Para desarrollo
        request.session['is_admin'] = is_admin_user
        request.session.modified = True
        return is_admin_user


@admin_required
@session_refresh  
def crear_noticia(request):
    """Vista para crear noticias - VERSIÓN CORREGIDA CON MEDIA_ROOT"""
    user_info = get_user_info(request)
    
    # Verificaciones de autenticación
    if 'user_id' not in request.session:
        return redirect('core:login')
    
    user_id = request.session.get('user_id')
    username = request.session.get('username', 'Usuario')
    comunidad_id = request.session.get('comunidad_id')
    admin_status = is_admin(request)
    
    if not admin_status:
        messages.error(request, "No tienes permisos para crear noticias.")
        return redirect('core:noticias')
    
    # Variables por defecto
    titulo = ""
    resumen = ""
    contenido = ""
    estado = "borrador"
    destacado = False
    error_message = None
    success_message = None
    
    # Verificar comunidad
    try:
        with connection.cursor() as cursor:
            if comunidad_id:
                try:
                    comunidad_id = int(comunidad_id)
                except (ValueError, TypeError):
                    print(f"Error al convertir ID de comunidad: {comunidad_id}")
                    comunidad_id = None
                
                if comunidad_id:
                    cursor.execute("""
                        SELECT id, nombre FROM raiz.comunidades WHERE id = %s
                    """, [comunidad_id])
                    
                    comunidad = cursor.fetchone()
                    if comunidad:
                        print(f"Usuario pertenece a la comunidad: {comunidad[1]} (ID: {comunidad[0]})")
                    else:
                        print(f"Comunidad con ID {comunidad_id} no encontrada")
                        comunidad_id = None
    except Exception as e:
        print(f"Error al verificar comunidad: {e}")
        comunidad_id = None
    
    # Procesar formulario
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        resumen = request.POST.get('resumen', '').strip()
        contenido = request.POST.get('contenido', '').strip()
        estado = request.POST.get('estado', 'borrador')
        destacado = request.POST.get('destacado') == 'on'
        
        # Validación básica
        if not titulo:
            error_message = "El título es obligatorio."
        elif not resumen:
            error_message = "El resumen es obligatorio."
        elif not contenido:
            error_message = "El contenido es obligatorio."
        else:
            try:
                with transaction.atomic():
                    # Generar slug único
                    base_slug = slugify(titulo)
                    slug = base_slug
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT COUNT(*) FROM raiz.noticias WHERE slug = %s",
                            [slug]
                        )
                        
                        if cursor.fetchone()[0] > 0:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                            random_suffix = str(uuid.uuid4())[:8]
                            slug = f"{base_slug}-{timestamp}-{random_suffix}"
                        
                        # Insertar noticia SIN imagen primero
                        cursor.execute("""
                            INSERT INTO raiz.noticias (
                                titulo, resumen, contenido, slug, estado, destacado,
                                fecha_creacion, fecha_actualizacion, fecha_publicacion,
                                imagen_portada, vistas, id_autor, id_comunidad
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s,
                                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,
                                CASE WHEN %s = 'publicado' THEN CURRENT_TIMESTAMP ELSE NULL END,
                                NULL, 0, %s, %s
                            ) RETURNING id
                        """, [
                            titulo, resumen, contenido, slug, estado, destacado,
                            estado, user_id, comunidad_id
                        ])
                        
                        noticia_id = cursor.fetchone()[0]
                        print(f"✅ Noticia creada con ID={noticia_id}, Slug={slug}")
                
                # 🔧 MANEJO CORREGIDO DE IMAGEN CON MEDIA_ROOT
                imagen_guardada = None
                imagen_error = None
                
                if 'imagen_portada' in request.FILES and request.FILES['imagen_portada']:
                    imagen = request.FILES['imagen_portada']
                    print(f"📸 Procesando imagen: {imagen.name} ({imagen.size} bytes)")
                    
                    try:
                        # Validar la imagen
                        if imagen.size > 10 * 1024 * 1024:  # 10MB max
                            imagen_error = "La imagen es demasiado grande (máximo 10MB)"
                        else:
                            _, extension = os.path.splitext(imagen.name)
                            extension = extension.lower()
                            
                            # Validar extensión
                            if extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                                imagen_error = "Formato de imagen no válido. Use JPG, PNG, GIF o WebP"
                            else:
                                # Generar nombre único para la imagen
                                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                                nombre_archivo = f"{slug}-{timestamp}{extension}"
                                
                                # 🔧 USAR MEDIA_ROOT en lugar de static
                                from django.conf import settings
                                ruta_guardado = os.path.join(settings.MEDIA_ROOT, 'news', nombre_archivo)
                                
                                # Crear directorio si no existe
                                os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
                                
                                # Guardar la imagen físicamente
                                print(f"💾 Guardando imagen en: {ruta_guardado}")
                                with open(ruta_guardado, 'wb+') as destino:
                                    for chunk in imagen.chunks():
                                        destino.write(chunk)
                                
                                # 🔧 GUARDAR PATH RELATIVO EN BD (news/imagen.jpg)
                                imagen_path_bd = f"news/{nombre_archivo}"
                                
                                # Actualizar la noticia con la ruta de la imagen
                                with connection.cursor() as cursor:
                                    cursor.execute("""
                                        UPDATE raiz.noticias 
                                        SET imagen_portada = %s 
                                        WHERE id = %s
                                    """, [imagen_path_bd, noticia_id])
                                
                                imagen_guardada = imagen_path_bd
                                print(f"✅ Imagen guardada y asociada: {imagen_path_bd}")
                                print(f"📁 Archivo físico en: {ruta_guardado}")
                                
                    except Exception as e:
                        imagen_error = f"Error al guardar imagen: {str(e)}"
                        print(f"❌ Error procesando imagen: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Preparar mensaje de éxito
                comunidad_texto = f" para la comunidad {comunidad_id}" if comunidad_id else ""
                success_message = f"Noticia '{titulo}' creada con éxito{comunidad_texto}."
                
                if imagen_guardada:
                    success_message += f" Imagen guardada correctamente en {imagen_guardada}."
                elif imagen_error:
                    success_message += f" Advertencia con imagen: {imagen_error}"
                elif 'imagen_portada' in request.FILES:
                    success_message += " Sin imagen seleccionada."
                
                # Limpiar formulario en caso de éxito
                titulo = ""
                resumen = ""
                contenido = ""
                estado = "borrador"
                destacado = False
                
            except Exception as e:
                print(f"❌ Error al crear noticia: {str(e)}")
                import traceback
                traceback.print_exc()
                error_message = f"Error al crear la noticia: {str(e)}"
    
    # Preparar contexto
    comunidad_nombre = "Sin comunidad asignada"
    if comunidad_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT nombre FROM raiz.comunidades WHERE id = %s
                """, [comunidad_id])
                result = cursor.fetchone()
                if result:
                    comunidad_nombre = result[0]
        except Exception as e:
            print(f"Error al obtener nombre de comunidad: {e}")
    
    context = {
        'error': error_message,
        'success': success_message,
        'form_data': {
            'titulo': titulo,
            'resumen': resumen,
            'contenido': contenido,
            'estado': estado,
            'destacado': destacado
        },
        'usuario': {
            'nombre': request.session.get('nombre', ''),
            'apellido': request.session.get('apellido', ''),
            'username': username
        },
        'comunidad': {
            'id': comunidad_id,
            'nombre': comunidad_nombre
        }
    }
    
    return render(request, 'core/create_news.html', context)


@admin_required
@session_refresh
def editar_noticia(request, slug):
    """Vista para editar noticias - VERSIÓN CORREGIDA CON MEDIA_ROOT"""
    user_info = get_user_info(request)
    
    # Verificar si el usuario es admin
    if not is_admin(request):
        messages.error(request, "No tienes permisos para editar noticias.")
        return redirect('core:noticias')
    
    # Obtener la noticia a editar
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT n.id, n.titulo, n.resumen, n.contenido, n.estado, n.destacado,
                       n.imagen_portada, n.id_comunidad, c.nombre as comunidad_nombre,
                       n.id_autor, u.nombre as autor_nombre, u.apellido as autor_apellido
                FROM raiz.noticias n
                LEFT JOIN raiz.comunidades c ON n.id_comunidad = c.id
                LEFT JOIN raiz.usuarios u ON n.id_autor = u.id
                WHERE n.slug = %s
            """, [slug])
            
            noticia_data = cursor.fetchone()
            
            if not noticia_data:
                messages.error(request, f"No se encontró la noticia con slug '{slug}'.")
                return redirect('core:noticias')
            
            # Mapeo de datos
            noticia = {
                'id': noticia_data[0],
                'titulo': noticia_data[1],
                'resumen': noticia_data[2],
                'contenido': noticia_data[3],
                'estado': noticia_data[4],
                'destacado': noticia_data[5],
                'imagen_portada': noticia_data[6],
                'id_comunidad': noticia_data[7],
                'comunidad_nombre': noticia_data[8],
                'id_autor': noticia_data[9],
                'autor_nombre': noticia_data[10],
                'autor_apellido': noticia_data[11],
                'slug': slug
            }
            
    except Exception as e:
        print(f"Error al obtener noticia: {e}")
        messages.error(request, f"Error al obtener la noticia: {e}")
        return redirect('core:noticias')
    
    # Procesar formulario si es POST
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        # Obtener datos del formulario
        titulo = request.POST.get('titulo', '').strip()
        resumen = request.POST.get('resumen', '').strip()
        contenido = request.POST.get('contenido', '').strip()
        estado = request.POST.get('estado', 'borrador')
        destacado = request.POST.get('destacado') == 'on'
        
        # Validación básica
        if not titulo:
            error_message = "El título es obligatorio."
        elif not resumen:
            error_message = "El resumen es obligatorio."
        elif not contenido:
            error_message = "El contenido es obligatorio."
        else:
            # Actualizar la noticia
            try:
                # Generar nuevo slug si cambió el título
                new_slug = slug
                if titulo != noticia['titulo']:
                    base_slug = slugify(titulo)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    random_suffix = str(uuid.uuid4())[:8]
                    new_slug = f"{base_slug}-{timestamp}-{random_suffix}"
                
                # Actualizar en la base de datos
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE raiz.noticias
                        SET titulo = %s, 
                            resumen = %s, 
                            contenido = %s, 
                            estado = %s, 
                            destacado = %s,
                            slug = %s,
                            fecha_actualizacion = CURRENT_TIMESTAMP,
                            fecha_publicacion = CASE 
                                WHEN %s = 'publicado' AND fecha_publicacion IS NULL 
                                THEN CURRENT_TIMESTAMP 
                                ELSE fecha_publicacion 
                            END
                        WHERE id = %s
                    """, [
                        titulo, 
                        resumen, 
                        contenido, 
                        estado, 
                        destacado,
                        new_slug,
                        estado,  # Para el CASE WHEN
                        noticia['id']
                    ])
                
                # 🔧 PROCESAR IMAGEN CORREGIDO CON MEDIA_ROOT
                imagen_actualizada = False
                imagen_error = None
                
                if 'imagen_portada' in request.FILES and request.FILES['imagen_portada']:
                    imagen = request.FILES['imagen_portada']
                    print(f"📸 Procesando nueva imagen: {imagen.name} ({imagen.size} bytes)")
                    
                    try:
                        # Validar la imagen
                        if imagen.size > 10 * 1024 * 1024:  # 10MB max
                            imagen_error = "La imagen es demasiado grande (máximo 10MB)"
                        else:
                            _, extension = os.path.splitext(imagen.name)
                            extension = extension.lower()
                            
                            # Validar extensión
                            if extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                                imagen_error = "Formato de imagen no válido. Use JPG, PNG, GIF o WebP"
                            else:
                                # Generar nombre único para la imagen
                                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                                nombre_archivo = f"{new_slug}-{timestamp}{extension}"
                                
                                # 🔧 USAR MEDIA_ROOT en lugar de static
                                from django.conf import settings
                                ruta_guardado = os.path.join(settings.MEDIA_ROOT, 'news', nombre_archivo)
                                
                                # Crear directorio si no existe
                                os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
                                
                                # 🔧 ELIMINAR IMAGEN ANTERIOR SI EXISTE
                                if noticia['imagen_portada']:
                                    try:
                                        ruta_anterior = os.path.join(settings.MEDIA_ROOT, noticia['imagen_portada'])
                                        if os.path.exists(ruta_anterior):
                                            os.remove(ruta_anterior)
                                            print(f"🗑️ Imagen anterior eliminada: {ruta_anterior}")
                                    except Exception as e:
                                        print(f"⚠️ No se pudo eliminar imagen anterior: {e}")
                                
                                # Guardar la nueva imagen
                                print(f"💾 Guardando nueva imagen en: {ruta_guardado}")
                                with open(ruta_guardado, 'wb+') as destino:
                                    for chunk in imagen.chunks():
                                        destino.write(chunk)
                                
                                # 🔧 GUARDAR PATH RELATIVO EN BD (news/imagen.jpg)
                                imagen_path_bd = f"news/{nombre_archivo}"
                                
                                # Actualizar el campo imagen_portada
                                with connection.cursor() as cursor:
                                    cursor.execute("""
                                        UPDATE raiz.noticias 
                                        SET imagen_portada = %s 
                                        WHERE id = %s
                                    """, [imagen_path_bd, noticia['id']])
                                
                                imagen_actualizada = True
                                print(f"✅ Nueva imagen guardada y asociada: {imagen_path_bd}")
                                print(f"📁 Archivo físico en: {ruta_guardado}")
                                
                    except Exception as e:
                        imagen_error = f"Error al actualizar imagen: {str(e)}"
                        print(f"❌ Error procesando imagen: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Mensaje de éxito
                success_message = f"Noticia '{titulo}' actualizada con éxito."
                
                if imagen_actualizada:
                    success_message += " Imagen actualizada correctamente."
                elif imagen_error:
                    success_message += f" Advertencia con imagen: {imagen_error}"
                
                # Redireccionar a la página de noticias en caso de éxito
                if new_slug != slug:
                    # Si cambió el slug, redirigir a la nueva URL
                    return redirect('core:editar_noticia', slug=new_slug)
                
            except Exception as e:
                print(f"Error al actualizar noticia: {e}")
                import traceback
                traceback.print_exc()
                error_message = f"Error al actualizar la noticia: {e}"
    
    # Preparar contexto para la plantilla
    context = {
        'error': error_message,
        'success': success_message,
        'noticia': noticia,
        'form_data': {
            'titulo': noticia['titulo'],
            'resumen': noticia['resumen'],
            'contenido': noticia['contenido'],
            'estado': noticia['estado'],
            'destacado': noticia['destacado']
        } if request.method != 'POST' else None,
        'usuario': {
            'nombre': request.session.get('nombre', ''),
            'apellido': request.session.get('apellido', ''),
            'username': request.session.get('username', '')
        },
        'comunidad': {
            'id': noticia['id_comunidad'],
            'nombre': noticia['comunidad_nombre']
        }
    }
    
    # Renderizar plantilla
    return render(request, 'core/edit_news.html', context)



@ajax_login_required
def like_noticia(request, noticia_id):
    """
    Vista para manejar el dar/quitar like a una noticia
    """
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_protect
    from django.utils.decorators import method_decorator
    from django.views.decorators.http import require_POST
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    # Identificar al usuario (desde la sesión o por IP si no está logueado)
    user_id = request.session.get('user_id')
    if not user_id:
        # Si no está logueado, usar la IP como identificador
        user_id = request.META.get('REMOTE_ADDR', 'anonymous')
    
    try:
        # Verificar si el usuario ya dio like a esta noticia
        from django.db import connection
        with connection.cursor() as cursor:
            # Verificar si existe la tabla de likes
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'raiz' 
                    AND table_name = 'noticia_likes'
                )
            """)
            
            likes_table_exists = cursor.fetchone()[0]
            
            # Si la tabla no existe, crearla
            if not likes_table_exists:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS raiz.noticia_likes (
                        id SERIAL PRIMARY KEY,
                        id_noticia VARCHAR(255) NOT NULL,
                        id_usuario VARCHAR(255) NOT NULL,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT unique_noticia_usuario UNIQUE(id_noticia, id_usuario)
                    )
                """)
                print("Tabla de likes creada")
            
            # Verificar si ya existe el like
            cursor.execute("""
                SELECT id FROM raiz.noticia_likes 
                WHERE id_noticia = %s AND id_usuario = %s
            """, [str(noticia_id), str(user_id)])
            
            like_existente = cursor.fetchone()
            
            if like_existente:
                # El usuario ya había dado like, entonces lo quitamos
                cursor.execute("""
                    DELETE FROM raiz.noticia_likes 
                    WHERE id_noticia = %s AND id_usuario = %s
                """, [str(noticia_id), str(user_id)])
                
                # Obtener nuevo conteo
                cursor.execute("""
                    SELECT COUNT(*) FROM raiz.noticia_likes 
                    WHERE id_noticia = %s
                """, [str(noticia_id)])
                nuevo_conteo = cursor.fetchone()[0]
                
                return JsonResponse({
                    'status': 'success',
                    'action': 'unliked',
                    'message': 'Like removido con éxito',
                    'new_count': nuevo_conteo
                })
            else:
                # El usuario no había dado like, así que lo agregamos
                cursor.execute("""
                    INSERT INTO raiz.noticia_likes (id_noticia, id_usuario)
                    VALUES (%s, %s)
                    ON CONFLICT (id_noticia, id_usuario) DO NOTHING
                """, [str(noticia_id), str(user_id)])
                
                # Obtener nuevo conteo
                cursor.execute("""
                    SELECT COUNT(*) FROM raiz.noticia_likes 
                    WHERE id_noticia = %s
                """, [str(noticia_id)])
                nuevo_conteo = cursor.fetchone()[0]
                
                return JsonResponse({
                    'status': 'success',
                    'action': 'liked',
                    'message': 'Like agregado con éxito',
                    'new_count': nuevo_conteo
                })
                
    except Exception as e:
        print(f"Error en like_noticia: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'Error al procesar el like: {str(e)}'
        }, status=500)
    

# Agregar esta función a core/views.py

@csrf_protect
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    Vista de logout mejorada que limpia mensajes apropiadamente.
    """
    user_id = request.session.get('user_id')
    username = request.session.get('username', 'Usuario desconocido')
    
    try:
        if user_id:
            logger.info(f"Logout: {username} (ID: {user_id})")
            
            # Opcional: Registrar logout en tabla de logs
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO raiz.logs (
                            id_usuario, 
                            accion, 
                            tabla_afectada, 
                            detalles, 
                            ip, 
                            user_agent, 
                            fecha
                        ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """, [
                        user_id,
                        'logout',
                        'usuarios',
                        'Cierre de sesión',
                        request.META.get('REMOTE_ADDR', ''),
                        request.META.get('HTTP_USER_AGENT', '')[:255]
                    ])
            except Exception as e:
                logger.warning(f"No se pudo registrar logout en logs: {e}")
        
        # Limpiar completamente la sesión
        request.session.flush()
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Sesión cerrada correctamente',
                'redirect': reverse('core:login')
            })
        
        # NUEVO: Agregar mensaje después de limpiar sesión pero SOLO para la página de login
        # No agregar mensaje aquí para evitar que persista en otras páginas
        
        # Redirigir directamente al login sin mensaje
        return redirect('core:login')
        
    except Exception as e:
        logger.error(f"Error durante logout: {e}")
        
        # Asegurar que la sesión se limpie aunque haya errores
        try:
            request.session.flush()
        except:
            pass
        
        # Si es AJAX, devolver error JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'Hubo un problema al cerrar la sesión',
                'redirect': reverse('core:login')
            }, status=500)
        
        # Para peticiones normales, redirigir sin mensaje
        return redirect('core:login')

@ajax_login_required
def check_session_status(request):
    user_info = get_user_info(request)
    """
    Vista AJAX para verificar el estado de la sesión.
    Útil para verificaciones periódicas desde el frontend.
    """
    from django.http import JsonResponse
    from django.utils import timezone
    
    try:
        is_logged_in = 'user_id' in request.session
        
        if is_logged_in:
            return JsonResponse({
                'status': 'active',
                'user_id': request.session.get('user_id'),
                'username': request.session.get('username'),
                'session_key': request.session.session_key,
                'timestamp': timezone.now().isoformat()
            })
        else:
            return JsonResponse({
                'status': 'expired',
                'message': 'Sesión no válida',
                'timestamp': timezone.now().isoformat()
            })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error al verificar sesión: {str(e)}'
        }, status=500)
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
import json
import datetime


@csrf_exempt
@require_POST
def session_extend(request):
    """
    Vista AJAX para extender la sesión del usuario.
    Permite resetear el temporizador de inactividad.
    """
    try:
        # Verificar que el usuario esté logueado
        if 'user_id' not in request.session:
            return JsonResponse({
                'status': 'error',
                'message': 'Usuario no logueado'
            }, status=401)
        
        # Renovar la sesión
        request.session.set_expiry(3600)  # Extender por 1 hora
        request.session['last_activity'] = datetime.datetime.now().timestamp()
        request.session.modified = True
        
        # Log de la extensión
        user_id = request.session.get('user_id')
        username = request.session.get('username', 'Usuario')
        
        logger.info(f"Sesión extendida para usuario {username} (ID: {user_id})")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Sesión extendida correctamente',
            'timestamp': datetime.datetime.now().isoformat(),
            'expires_in': 3600
        })
        
    except Exception as e:
        logger.error(f"Error al extender sesión: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al extender sesión: {str(e)}'
        }, status=500)


def check_session_status(request):
    """
    Vista AJAX para verificar el estado de la sesión.
    Útil para verificaciones periódicas desde el frontend.
    """
    try:
        is_logged_in = 'user_id' in request.session
        
        if is_logged_in:
            # Verificar si la sesión ha expirado por inactividad
            last_activity = request.session.get('last_activity')
            current_time = datetime.datetime.now().timestamp()
            
            # Si han pasado más de 1 hora desde la última actividad
            if last_activity and (current_time - last_activity) > 3600:
                # Limpiar sesión expirada
                request.session.flush()
                return JsonResponse({
                    'status': 'expired',
                    'message': 'Sesión expirada por inactividad',
                    'timestamp': datetime.datetime.now().isoformat()
                })
            
            # Actualizar última actividad
            request.session['last_activity'] = current_time
            request.session.modified = True
            
            return JsonResponse({
                'status': 'active',
                'user_id': request.session.get('user_id'),
                'username': request.session.get('username'),
                'session_key': request.session.session_key,
                'timestamp': datetime.datetime.now().isoformat(),
                'last_activity': last_activity
            })
        else:
            return JsonResponse({
                'status': 'expired',
                'message': 'Sesión no válida',
                'timestamp': datetime.datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error al verificar sesión: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al verificar sesión: {str(e)}'
        }, status=500)


# ===================================
# DECORADORES PERSONALIZADOS (si no existen)
# ===================================

def login_required_custom(view_func):
    """
    Decorador personalizado para verificar autenticación vía sesión
    """
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            logger.warning(f"Acceso denegado a {request.path} - Usuario no autenticado")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'No autenticado',
                    'redirect': reverse('core:login')
                }, status=401)
            return redirect('core:login')
        
        # Verificar si la sesión ha expirado
        last_activity = request.session.get('last_activity')
        if last_activity:
            current_time = datetime.datetime.now().timestamp()
            if (current_time - last_activity) > 3600:  # 1 hora
                request.session.flush()
                logger.info(f"Sesión expirada para usuario - redirigiendo al login")
                return redirect('core:login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorador para verificar que el usuario sea administrador
    """
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('core:login')
        
        # Verificar si es admin
        if not is_admin(request):
            logger.warning(f"Acceso admin denegado a {request.path} - Usuario: {request.session.get('username')}")
            messages.error(request, "No tienes permisos de administrador.")
            return redirect('core:marketplace')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def ajax_login_required(view_func):
    """
    Decorador para vistas AJAX que requieren autenticación
    """
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return JsonResponse({
                'status': 'error',
                'message': 'No autenticado',
                'redirect': reverse('core:login')
            }, status=401)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def session_refresh(view_func):
    """
    Decorador para actualizar la actividad de la sesión
    """
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            request.session['last_activity'] = datetime.datetime.now().timestamp()
            request.session.modified = True
        
        return view_func(request, *args, **kwargs)
    return wrapper


def get_user_info(request):
    """
    Función helper para obtener información del usuario de la sesión
    """
    return {
        'user_id': request.session.get('user_id'),
        'username': request.session.get('username', ''),
        'nombre': request.session.get('nombre', ''),
        'apellido': request.session.get('apellido', ''),
        'comunidad_id': request.session.get('comunidad_id'),
        'comunidad_nombre': request.session.get('comunidad_nombre', ''),
        'is_admin': request.session.get('is_admin', False)
    }

# En core/views.py - ELIMINAR la función register simple y usar solo esta:

@csrf_protect
def register(request):
    """Vista de registro que funciona tanto en local como en producción"""
    
    # LIMPIAR MENSAJES DE OTRAS VISTAS
    storage = messages.get_messages(request)
    for message in storage:
        pass
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '')
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        biografia = request.POST.get('biografia', '').strip()
        id_comunidad = request.POST.get('id_comunidad', '')
        
        # Lista de errores
        errors = []
        
        # Validaciones
        if not nombre:
            errors.append("El nombre es requerido")
        elif len(nombre) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres")
            
        if not apellido:
            errors.append("El apellido es requerido")
        elif len(apellido) < 2:
            errors.append("El apellido debe tener al menos 2 caracteres")
            
        if not username:
            errors.append("El nombre de usuario es requerido")
        elif len(username) < 3:
            errors.append("El nombre de usuario debe tener al menos 3 caracteres")
        elif not username.replace('_', '').isalnum():
            errors.append("El nombre de usuario solo puede contener letras, números y guiones bajos")
            
        if not email:
            errors.append("El email es requerido")
        elif '@' not in email or '.' not in email:
            errors.append("El email no tiene un formato válido")
            
        if not password:
            errors.append("La contraseña es requerida")
        elif len(password) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")
            
        if password != password_confirm:
            errors.append("Las contraseñas no coinciden")
            
        if not id_comunidad:
            errors.append("Debes seleccionar una comunidad")
            
        # Validar fecha de nacimiento
        if fecha_nacimiento:
            try:
                from datetime import datetime, date
                fecha_obj = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
                today = date.today()
                age = today.year - fecha_obj.year - ((today.month, today.day) < (fecha_obj.month, fecha_obj.day))
                if age < 18:
                    errors.append("Debes ser mayor de 18 años para registrarte")
            except ValueError:
                errors.append("Fecha de nacimiento inválida")
        
        # Verificar unicidad de usuario y email
        if not errors:
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    # Verificar usuario existente
                    cursor.execute("SELECT id FROM raiz.usuarios WHERE username = %s", [username])
                    if cursor.fetchone():
                        errors.append("El nombre de usuario ya está en uso")
                    
                    # Verificar email existente
                    cursor.execute("SELECT id FROM raiz.usuarios WHERE email = %s", [email])
                    if cursor.fetchone():
                        errors.append("El email ya está registrado")
                    
                    # Verificar que la comunidad existe
                    cursor.execute("SELECT id FROM raiz.comunidades WHERE id = %s AND activo = true", [id_comunidad])
                    if not cursor.fetchone():
                        errors.append("La comunidad seleccionada no es válida")
                        
            except Exception as e:
                logger.error(f"Error verificando datos únicos: {e}")
                errors.append("Error al verificar datos. Intenta nuevamente.")
        
        # Si no hay errores, crear el usuario
        if not errors:
            try:
                from django.contrib.auth.hashers import make_password
                from django.db import transaction
                from django.conf import settings
                import uuid
                
                # DETECCIÓN AUTOMÁTICA DEL ENTORNO
                is_atomic_requests = getattr(settings, 'DATABASES', {}).get('default', {}).get('ATOMIC_REQUESTS', False)
                
                # MÉTODO UNIVERSAL: Funciona con o sin ATOMIC_REQUESTS
                def create_user():
                    # Generar ID único
                    user_id = str(uuid.uuid4())
                    
                    # Hashear la contraseña
                    hashed_password = make_password(password)
                    
                    # Insertar usuario
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO raiz.usuarios (
                                id, username, password, email, nombre, apellido,
                                fecha_nacimiento, telefono, direccion, biografia,
                                id_comunidad, fecha_registro, activo, verificado
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                CURRENT_TIMESTAMP, true, false
                            )
                        """, [
                            user_id, username, hashed_password, email, nombre, apellido,
                            fecha_nacimiento if fecha_nacimiento else None,
                            telefono if telefono else None,
                            direccion if direccion else None,
                            biografia if biografia else None,
                            int(id_comunidad)
                        ])
                        
                        # RETORNAR EL ID del usuario creado
                        return user_id
                
                # EJECUTAR SEGÚN EL ENTORNO
                if is_atomic_requests:
                    # PRODUCCIÓN: Django maneja las transacciones automáticamente
                    logger.info("Usando transacciones automáticas (ATOMIC_REQUESTS=True)")
                    user_id = create_user()
                else:
                    # LOCAL: Usar transacción manual de Django
                    logger.info("Usando transacciones manuales (ATOMIC_REQUESTS=False)")
                    with transaction.atomic():
                        user_id = create_user()
                
                # Log del registro exitoso
                logger.info(f"Usuario registrado exitosamente: {username} ({email}) con ID: {user_id}")
                
                # Renderizar con éxito
                form_data = {
                    'nombre': nombre,
                    'apellido': apellido,
                    'username': username,
                    'email': email,
                    'fecha_nacimiento': fecha_nacimiento,
                    'telefono': telefono,
                    'direccion': direccion,
                    'biografia': biografia,
                    'id_comunidad': id_comunidad
                }
                
                return render(request, 'core/register.html', {
                    'success': True,
                    'form_data': form_data,
                    'comunidades': obtener_comunidades(),
                    'registration_success': True
                })
                
            except Exception as e:
                logger.error(f"Error creando usuario: {e}")
                import traceback
                traceback.print_exc()
                errors.append(f"Error al crear la cuenta: {str(e)}")
        
        # Si hay errores, mostrarlos
        if errors:
            form_data = {
                'nombre': nombre,
                'apellido': apellido,
                'username': username,
                'email': email,
                'fecha_nacimiento': fecha_nacimiento,
                'telefono': telefono,
                'direccion': direccion,
                'biografia': biografia,
                'id_comunidad': id_comunidad
            }
            
            return render(request, 'core/register.html', {
                'errors': errors,
                'form_data': form_data,
                'comunidades': obtener_comunidades()
            })
    
    # GET request - mostrar formulario
    return render(request, 'core/register.html', {
        'comunidades': obtener_comunidades()
    })


def obtener_comunidades():
    """Función helper para obtener comunidades activas"""
    try:
        comunidades = []
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, region, pais 
                FROM raiz.comunidades 
                WHERE activo = true 
                ORDER BY nombre
            """)
            
            for row in cursor.fetchall():
                comunidad_id, nombre, region, pais = row
                display_name = f"{nombre}"
                if region:
                    display_name += f" - {region}"
                if pais:
                    display_name += f" ({pais})"
                    
                comunidades.append({
                    'id': comunidad_id,
                    'nombre': nombre,
                    'display_name': display_name
                })
        
        return comunidades
    except Exception as e:
        logger.error(f"Error obteniendo comunidades: {e}")
        return []

def send_verification_email(user_id, email, username):
    """
    Función para enviar email de verificación (implementar más tarde)
    """
    # TODO: Implementar envío de email
    # Por ahora solo log
    logger.info(f"Email de verificación debe enviarse a {email} para usuario {username}")
    pass


import os
from django.conf import settings
import uuid
import datetime

def handle_uploaded_file(uploaded_file, category='general'):
    """
    Maneja la subida de archivos de forma robusta.
    
    Args:
        uploaded_file: Archivo subido desde el formulario
        category: Categoría del archivo ('news', 'profiles', etc.)
    
    Returns:
        str: Ruta relativa del archivo guardado o None si hay error
    """
    try:
        # Validar que el archivo no esté vacío
        if not uploaded_file or uploaded_file.size == 0:
            print("❌ Archivo vacío o no válido")
            return None
        
        # Validar tamaño máximo (5MB)
        if uploaded_file.size > 5 * 1024 * 1024:
            print(f"❌ Archivo muy grande: {uploaded_file.size} bytes")
            return None
        
        # Obtener extensión del archivo
        name, extension = os.path.splitext(uploaded_file.name)
        
        # Validar extensiones permitidas
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        if extension.lower() not in allowed_extensions:
            print(f"❌ Extensión no permitida: {extension}")
            return None
        
        # Generar nombre único para evitar colisiones
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{category}_{timestamp}_{unique_id}{extension}"
        
        # Determinar la ruta donde guardar
        category_dir = os.path.join(settings.MEDIA_ROOT, category)
        os.makedirs(category_dir, exist_ok=True)
        
        file_path = os.path.join(category_dir, filename)
        relative_path = f"{category}/{filename}"  # Para guardar en la BD
        
        # Guardar el archivo
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        print(f"✅ Archivo guardado: {file_path}")
        print(f"✅ Ruta relativa: {relative_path}")
        
        return relative_path
        
    except Exception as e:
        print(f"❌ Error al guardar archivo: {e}")
        import traceback
        traceback.print_exc()
        return None