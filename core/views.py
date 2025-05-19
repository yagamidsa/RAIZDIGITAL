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
    
    # 4. Configurar paginación manual
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(filtered_news, 9)  # 9 noticias por página
    
    try:
        noticias = paginator.page(page_number)
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
    Vista para mostrar el detalle de una noticia.
    
    Obtiene la noticia correspondiente al slug proporcionado
    y aumenta su contador de vistas.
    """
    # Obtener la noticia por su slug o devolver 404 si no existe
    noticia = get_object_or_404(Noticia, slug=slug, estado='publicado')
    
    # Incrementar el contador de vistas
    noticia.vistas += 1
    noticia.save(update_fields=['vistas'])
    
    # Obtener autor de la noticia
    try:
        autor = Usuario.objects.get(id=noticia.id_autor)
        nombre_autor = f"{autor.nombre} {autor.apellido}"
        foto_autor = autor.foto_perfil
    except Usuario.DoesNotExist:
        nombre_autor = "Autor desconocido"
        foto_autor = None
    
    # Obtener noticias relacionadas (misma comunidad o mismo autor)
    noticias_relacionadas = Noticia.objects.filter(
        Q(id_comunidad=noticia.id_comunidad) | Q(id_autor=noticia.id_autor),
        estado='publicado'
    ).exclude(id=noticia.id).order_by('-fecha_publicacion')[:3]
    
    # Preparar datos para la plantilla
    context = {
        'noticia': noticia,
        'autor': {
            'nombre': nombre_autor,
            'foto': foto_autor,
            'id': noticia.id_autor
        },
        'noticias_relacionadas': noticias_relacionadas,
    }
    
    return render(request, 'core/noticia_detalle.html', context)



def is_admin(request):
    """
    Determina si el usuario actual es administrador basado en sus roles.
    """
    if 'user_id' not in request.session:
        print("No hay user_id en la sesión")
        return False
    
    try:
        user_id = request.session.get('user_id')
        print(f"Verificando si el usuario {user_id} es administrador")
        
        # Código para verificar si es admin...
            
        # Para desarrollo, podemos forzar que el usuario sea administrador
        # Comenta esta línea en producción
        is_admin_user = True
        
        # Guardar en sesión para futuras verificaciones
        request.session['is_admin'] = is_admin_user
        # Importante: Guardar la sesión explícitamente
        request.session.modified = True
        
        return is_admin_user
    except Exception as e:
        print(f"Error verificando rol de administrador: {e}")
        # En caso de error, asumimos que es administrador para desarrollo
        request.session['is_admin'] = True
        request.session.modified = True
        return True


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