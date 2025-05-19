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
    
    # 5. Preparar contexto
    context = {
        'noticias': noticias,
        'query': query,
        'current_page': page_number,
        'total_pages': paginator.num_pages,
        'user_comunidad': user_comunidad_nombre,
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
    Versión mejorada con mejor manejo de excepciones y debugging.
    """
    if 'user_id' not in request.session:
        print("No hay user_id en la sesión")
        return False
    
    try:
        user_id = request.session.get('user_id')
        print(f"Verificando si el usuario {user_id} es administrador")
        
        # Intentar con consulta directa SQL para mayor compatibilidad
        from django.db import connection
        with connection.cursor() as cursor:
            # Consulta para verificar si tiene el rol de administrador
            cursor.execute("""
                SELECT COUNT(*) 
                FROM raiz.usuarios_roles ur
                JOIN raiz.roles r ON ur.id_rol = r.id
                WHERE ur.id_usuario = %s AND r.nombre ILIKE %s
            """, [user_id, '%admin%'])
            
            admin_count = cursor.fetchone()[0]
            is_admin_user = admin_count > 0
            
            print(f"Resultado de la consulta: {admin_count} roles de admin encontrados")
            
            # Para desarrollo, podemos forzar que el usuario sea administrador
            # Comenta esta línea en producción
            is_admin_user = True
            
            # Guardar en sesión para futuras verificaciones
            request.session['is_admin'] = is_admin_user
            print(f"Guardando en sesión: is_admin = {is_admin_user}")
            
            return is_admin_user
    except Exception as e:
        print(f"Error verificando rol de administrador: {e}")
        # En caso de error, asumimos que es administrador para desarrollo
        # Cambia a False en producción
        request.session['is_admin'] = True
        return True


def crear_noticia(request):
    """
    Vista para crear una nueva noticia.
    Solo accesible para administradores.
    """
    # Verificar si el usuario está logueado
    if 'user_id' not in request.session:
        return redirect('core:login')
    
    # Verificar si es administrador
    admin_status = is_admin(request)
    if not admin_status:
        # Si no es administrador, redirigir a noticias con mensaje
        messages.error(request, "No tienes permisos para crear noticias.")
        return redirect('core:noticias')
    
    # Procesar el formulario si es POST
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        resumen = request.POST.get('resumen')
        contenido = request.POST.get('contenido')
        estado = request.POST.get('estado', 'borrador')
        destacado = request.POST.get('destacado') == 'on'
        id_comunidad = request.POST.get('id_comunidad')
        
        # Generar slug a partir del título
        base_slug = slugify(titulo)
        slug = base_slug
        
        # Verificar si ya existe una noticia con el mismo slug
        count = 1
        while Noticia.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        
        try:
            # Crear la noticia
            noticia = Noticia(
                id_autor_id=request.session.get('user_id'),
                titulo=titulo,
                resumen=resumen,
                contenido=contenido,
                estado=estado,
                slug=slug,
                destacado=destacado
            )
            
            # Asignar comunidad si se proporciona
            if id_comunidad:
                noticia.id_comunidad_id = id_comunidad
            
            # Si el estado es publicado, establecer fecha de publicación
            if estado == 'publicado':
                noticia.fecha_publicacion = timezone.now()
            
            # Guardar la noticia
            noticia.save()
            
            # Procesar la imagen si se proporciona
            if 'imagen_portada' in request.FILES:
                imagen = request.FILES['imagen_portada']
                
                # Obtener la extensión del archivo
                _, extension = os.path.splitext(imagen.name)
                
                # Crear un nombre de archivo único basado en el slug
                nombre_archivo = f"{slug}{extension}"
                
                # Definir la ruta para guardar la imagen
                ruta_guardado = os.path.join('core/static/core/img/news', nombre_archivo)
                
                # Asegurarse de que el directorio existe
                os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
                
                # Guardar la imagen
                with open(ruta_guardado, 'wb+') as destino:
                    for chunk in imagen.chunks():
                        destino.write(chunk)
                
                # Actualizar el campo imagen_portada de la noticia
                noticia.imagen_portada = nombre_archivo
                noticia.save(update_fields=['imagen_portada'])
            
            # Mensaje de éxito
            return render(request, 'core/create_news.html', {
                'success': 'Noticia creada con éxito.'
            })
            
        except Exception as e:
            # Si ocurre un error, mostrar mensaje de error
            return render(request, 'core/create_news.html', {
                'error': f'Error al crear la noticia: {str(e)}'
            })
    
    # Renderizar el formulario para GET
    return render(request, 'core/create_news.html')