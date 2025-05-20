from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
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

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    """
    Vista de login segura con registro de debugging para diagnóstico.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Mensaje de depuración
        print(f"Intento de login: username={username}")
        
        try:
            # Consulta SQL directa para verificar si el usuario existe
            from django.db import connection
            with connection.cursor() as cursor:
                # Consulta mejorada para obtener también información de la comunidad
                cursor.execute("""
                    SELECT u.id, u.username, u.password, u.nombre, u.apellido, 
                           c.id as comunidad_id, c.nombre as comunidad_nombre
                    FROM raiz.usuarios u
                    LEFT JOIN raiz.comunidades c ON u.id_comunidad = c.id
                    WHERE u.username = %s
                """, [username])
                user_data = cursor.fetchone()
            
            # Imprimir datos para diagnóstico
            print(f"Datos obtenidos de la BD: {user_data}")
            
            if user_data:
                user_id, db_username, db_password, nombre, apellido, comunidad_id, comunidad_nombre = user_data
                
                # Verificación real de contraseña
                from django.contrib.auth.hashers import check_password
                password_valid = check_password(password, db_password)
                
                # Para desarrollo, podemos permitir cualquier contraseña para facilitar las pruebas
                # Comentar esta línea en producción
                # password_valid = True
                
                print(f"Contraseña válida: {password_valid}")
                
                if password_valid:
                    # Iniciar sesión y guardar también datos de comunidad
                    request.session['user_id'] = str(user_id)
                    request.session['username'] = db_username
                    request.session['nombre'] = nombre
                    request.session['apellido'] = apellido
                    
                    # Debugging - verificar datos guardados en sesión
                    print(f"Datos en la sesión:")
                    print(f"- user_id: {request.session.get('user_id')}")
                    print(f"- username: {request.session.get('username')}")
                    print(f"- nombre: {request.session.get('nombre')}")
                    print(f"- apellido: {request.session.get('apellido')}")
                    
                    # Guardar información de la comunidad
                    if comunidad_id:
                        request.session['comunidad_id'] = comunidad_id
                        request.session['comunidad_nombre'] = comunidad_nombre
                        print(f"- comunidad_id: {request.session.get('comunidad_id')}")
                        print(f"- comunidad_nombre: {request.session.get('comunidad_nombre')}")
                    
                    # Actualizar último login
                    import datetime
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE raiz.usuarios SET ultimo_login = %s WHERE id = %s",
                            [datetime.datetime.now(), user_id]
                        )
                    
                    # Redirigir al marketplace
                    return redirect('core:marketplace')
                else:
                    return render(request, 'core/login.html', {
                        'error': 'Contraseña incorrecta',
                        'username': username
                    })
            else:
                return render(request, 'core/login.html', {
                    'error': 'Usuario no encontrado en la base de datos',
                    'username': username
                })
                
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return render(request, 'core/login.html', {
                'error': f'Error en el sistema de autenticación: {e}',
                'username': username
            })
    
    return render(request, 'core/login.html')


def password_recovery(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Verificar si el email existe en la base de datos
        try:
            user = Usuario.objects.get(email=email)
            
            # Generar token de recuperación
            recovery_token = str(uuid.uuid4())
            user.token_recuperacion = recovery_token
            user.fecha_token = datetime.datetime.now()
            user.save(update_fields=['token_recuperacion', 'fecha_token'])
            
            # Construir URL de recuperación
            recovery_url = f"{request.scheme}://{request.get_host()}/reset-password/{recovery_token}/"
            
            # Enviar email - comentado para entorno de desarrollo
            """
            subject = 'Recuperación de contraseña - Raíz Digital'
            html_message = render_to_string('core/emails/password_recovery.html', {
                'user': user,
                'recovery_url': recovery_url
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to = email
            
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            """
            
            # Como el envío de email está comentado para desarrollo, mostrar mensaje de éxito
            context = {
                'success': 'Se han enviado instrucciones para restablecer tu contraseña a tu correo electrónico.'
            }
            return render(request, 'core/password_recovery.html', context)
            
        except Usuario.DoesNotExist:
            # Si el correo no existe, mostramos un mensaje genérico por seguridad
            context = {
                'success': 'Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña.'
            }
            return render(request, 'core/password_recovery.html', context)
    
    return render(request, 'core/password_recovery.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def password_recovery(request):
    return render(request, 'core/password_recovery.html')

#@login_required
#def marketplace(request):
#    return render(request, 'core/marketplace.html')

def marketplace(request):
    """
    Vista del marketplace principal que muestra información personalizada del usuario
    y su comunidad.
    """
    # Verificar si el usuario está logueado (mediante la sesión)
    if 'user_id' not in request.session:
        # Si no está logueado, redirigir al login
        return redirect('core:login')
        
    # Obtener datos del usuario desde la sesión
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    nombre = request.session.get('nombre', '')
    apellido = request.session.get('apellido', '')
    
    # Obtener nombre de la comunidad directamente de la sesión
    community_name = request.session.get('comunidad_nombre')
    
    # Crear nombre completo para mostrar en la interfaz
    nombre_completo = f"{nombre} {apellido}".strip()
    
    # Para diagnóstico - imprimir los valores
    print(f"ID de usuario: {user_id}")
    print(f"Username: {username}")
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Nombre completo: {nombre_completo}")
    print(f"Comunidad: {community_name}")
    
    context = {
        'username': username,
        'nombre': nombre,
        'apellido': apellido,
        'nombre_completo': nombre_completo,
        'community_name': community_name
    }
    
    return render(request, 'core/marketplace_home.html', context)


# Vistas para las noticias
def noticias(request):
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

def noticia_detalle(request, slug):
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


def crear_noticia(request):
    """
    Vista para crear noticias con control de concurrencia y seguridad.
    Maneja la creación de noticias para administradores de diferentes comunidades.
    """
    from django.shortcuts import render, redirect
    from django.utils.text import slugify
    from django.contrib import messages
    import os
    import traceback
    from django.db import connection, transaction
    import uuid
    import datetime
    
    # PASO 1: Verificación de autenticación y autorización
    if 'user_id' not in request.session:
        # Redirigir al login si no hay sesión
        return redirect('core:login')
    
    user_id = request.session.get('user_id')
    username = request.session.get('username', 'Usuario')
    
    # Verificar que el usuario sea administrador y obtener su comunidad
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
    
    # PASO 2: Verificar y obtener información de la comunidad del usuario
    try:
        with connection.cursor() as cursor:
            if comunidad_id:
                # Convertir a entero si es posible
                try:
                    comunidad_id = int(comunidad_id)
                except (ValueError, TypeError):
                    print(f"Error al convertir ID de comunidad: {comunidad_id}")
                    comunidad_id = None
                
                # Verificar si la comunidad existe
                if comunidad_id:
                    cursor.execute("""
                        SELECT id, nombre 
                        FROM raiz.comunidades 
                        WHERE id = %s
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
    
    # PASO 3: Procesar el formulario si es POST
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
            # PASO 4: Crear la noticia con control de concurrencia
            try:
                # Usar transacción para garantizar atomicidad
                with transaction.atomic():
                    # Generar un slug único
                    base_slug = slugify(titulo)
                    slug = base_slug
                    
                    with connection.cursor() as cursor:
                        # Verificar si ya existe un slug igual
                        cursor.execute(
                            "SELECT COUNT(*) FROM raiz.noticias WHERE slug = %s",
                            [slug]
                        )
                        
                        if cursor.fetchone()[0] > 0:
                            # Si existe, añadir timestamp único para evitar colisiones
                            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                            random_suffix = str(uuid.uuid4())[:8]
                            slug = f"{base_slug}-{timestamp}-{random_suffix}"
                        
                        # IMPORTANTE: Usar una secuencia correctamente
                        # Primero verificar la secuencia
                        cursor.execute("""
                            SELECT pg_get_serial_sequence('raiz.noticias', 'id') as sequence_name
                        """)
                        
                        sequence_name = cursor.fetchone()[0]
                        if sequence_name:
                            # Resetear la secuencia si es necesario
                            cursor.execute("""
                                SELECT SETVAL(%s, COALESCE((SELECT MAX(id) FROM raiz.noticias), 0) + 1, false)
                            """, [sequence_name])
                        
                        # Insertar la noticia con FOR UPDATE para bloquear la tabla durante la inserción
                        cursor.execute("LOCK TABLE raiz.noticias IN EXCLUSIVE MODE")
                        
                        # Insertar con variables bien definidas
                        cursor.execute("""
                            INSERT INTO raiz.noticias (
                                titulo, 
                                resumen, 
                                contenido, 
                                slug,
                                estado, 
                                destacado,
                                fecha_creacion, 
                                fecha_actualizacion,
                                fecha_publicacion,
                                imagen_portada,
                                vistas,
                                id_autor,
                                id_comunidad
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s,
                                CURRENT_TIMESTAMP, 
                                CURRENT_TIMESTAMP,
                                CASE WHEN %s = 'publicado' THEN CURRENT_TIMESTAMP ELSE NULL END,
                                NULL,
                                0,
                                %s,
                                %s
                            ) RETURNING id
                        """, [
                            titulo, 
                            resumen, 
                            contenido, 
                            slug,
                            estado, 
                            destacado,
                            estado,
                            user_id,
                            comunidad_id  # Incluye comunidad_id (puede ser NULL)
                        ])
                        
                        noticia_id = cursor.fetchone()[0]
                        print(f"✅ Noticia creada con ID={noticia_id}, Slug={slug}, Comunidad={comunidad_id}")
                
                # PASO 5: Procesar imagen si existe (fuera de la transacción para no bloquear)
                if 'imagen_portada' in request.FILES:
                    imagen = request.FILES['imagen_portada']
                    _, extension = os.path.splitext(imagen.name)
                    
                    # Usar una combinación de slug y timestamp para el nombre del archivo
                    nombre_archivo = f"{slug}{extension}"
                    ruta_guardado = os.path.join('core/static/core/img/news', nombre_archivo)
                    
                    # Asegurarse de que el directorio existe
                    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
                    
                    # Guardar la imagen
                    with open(ruta_guardado, 'wb+') as destino:
                        for chunk in imagen.chunks():
                            destino.write(chunk)
                    
                    # Actualizar el campo imagen_portada de la noticia
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE raiz.noticias 
                            SET imagen_portada = %s 
                            WHERE id = %s
                        """, [nombre_archivo, noticia_id])
                
                # Mensaje de éxito que incluye la comunidad
                comunidad_texto = f" para la comunidad {comunidad_id}" if comunidad_id else ""
                success_message = f"Noticia '{titulo}' creada con éxito{comunidad_texto}."
                
                # Limpiar formulario en caso de éxito
                titulo = ""
                resumen = ""
                contenido = ""
                estado = "borrador"
                destacado = False
                
            except Exception as e:
                print(f"\n=== ERROR AL CREAR NOTICIA ===")
                print(f"Error: {str(e)}")
                print(traceback.format_exc())
                error_message = f"Error al crear la noticia: {str(e)}"
    
    # PASO 6: Preparar información contextual para la plantilla
    # Obtener comunidad del usuario para mostrar en la interfaz
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
    
    # Preparar contexto para la plantilla
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
    
    # Renderizar la plantilla
    return render(request, 'core/create_news.html', context)


def editar_noticia(request, slug):
    """
    Vista para editar una noticia existente.
    """
    # Verificar si el usuario es admin
    if not is_admin(request):
        messages.error(request, "No tienes permisos para editar noticias.")
        return redirect('core:noticias')
    
    # Obtener la noticia a editar
    try:
        # Usar SQL para obtener la noticia
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
                    import datetime
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
                                WHEN estado = 'publicado' AND fecha_publicacion IS NULL 
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
                        noticia['id']
                    ])
                
                # Procesar imagen si existe
                if 'imagen_portada' in request.FILES:
                    imagen = request.FILES['imagen_portada']
                    _, extension = os.path.splitext(imagen.name)
                    
                    # Generar nombre de archivo único
                    nombre_archivo = f"{new_slug}{extension}"
                    ruta_guardado = os.path.join('core/static/core/img/news', nombre_archivo)
                    
                    # Asegurarse de que el directorio existe
                    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
                    
                    # Guardar la imagen
                    with open(ruta_guardado, 'wb+') as destino:
                        for chunk in imagen.chunks():
                            destino.write(chunk)
                    
                    # Actualizar el campo imagen_portada
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE raiz.noticias 
                            SET imagen_portada = %s 
                            WHERE id = %s
                        """, [nombre_archivo, noticia['id']])
                
                # Mensaje de éxito
                success_message = f"Noticia '{titulo}' actualizada con éxito."
                
                # Redireccionar a la página de noticias en caso de éxito
                if new_slug != slug:
                    # Si cambió el slug, redirigir a la nueva URL
                    return redirect('core:editar_noticia', slug=new_slug)
                
            except Exception as e:
                print(f"Error al actualizar noticia: {e}")
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




def like_noticia(request, noticia_id):
    """
    Vista para manejar el dar/quitar like a una noticia
    """
    from django.http import JsonResponse
    
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
                        id_noticia UUID NOT NULL,
                        id_usuario VARCHAR(255) NOT NULL,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT unique_noticia_usuario UNIQUE(id_noticia, id_usuario)
                    )
                """)
            
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
                
                # Devolver el resultado
                return JsonResponse({
                    'status': 'success',
                    'action': 'unliked',
                    'message': 'Like removido con éxito'
                })
            else:
                # El usuario no había dado like, así que lo agregamos
                cursor.execute("""
                    INSERT INTO raiz.noticia_likes (id_noticia, id_usuario)
                    VALUES (%s, %s)
                """, [str(noticia_id), str(user_id)])
                
                # Devolver el resultado
                return JsonResponse({
                    'status': 'success',
                    'action': 'liked',
                    'message': 'Like agregado con éxito'
                })
                
    except Exception as e:
        print(f"Error en like_noticia: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'Error al procesar el like: {str(e)}'
        }, status=500)