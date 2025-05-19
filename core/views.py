from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
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
from .models import *

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    """
    Vista de login segura que solo permite acceso a usuarios reales 
    que existen en la base de datos.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Mensaje de depuración (opcional, remover en producción)
        print(f"Intento de login: username={username}")
        
        try:
            # Consulta SQL directa para verificar si el usuario existe
            from django.db import connection
            with connection.cursor() as cursor:
                # Consultar la tabla de usuarios directamente
                # Ajusta el nombre de la tabla según sea necesario
                cursor.execute("SELECT id, username, password, nombre, apellido FROM raiz.usuarios WHERE username = %s", [username])
                user_data = cursor.fetchone()
            
            if user_data:
                user_id, db_username, db_password, nombre, apellido = user_data
                
                # En desarrollo, permitir cualquier contraseña (remover en producción)
                # print("⚠️ MODO DESARROLLO: No se verifica contraseña")
                # password_valid = True
                
                # Verificación real de contraseña
                from django.contrib.auth.hashers import check_password
                password_valid = check_password(password, db_password)
                
                if password_valid:
                    # Iniciar sesión
                    request.session['user_id'] = str(user_id)
                    request.session['username'] = db_username
                    request.session['nombre'] = nombre
                    request.session['apellido'] = apellido
                    
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
                'error': 'Error en el sistema de autenticación',
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
    # Verificar si el usuario está logueado (mediante la sesión)
    if 'user_id' not in request.session:
        # Si no está logueado, redirigir al login
        return redirect('core:login')
        
    # Obtener datos del usuario desde la sesión
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    nombre = request.session.get('nombre')
    
    # Intentar obtener datos de la comunidad del usuario si existe
    community_name = None
    try:
        user = Usuario.objects.get(id=user_id)
        if user.id_comunidad:
            community_name = user.id_comunidad.nombre
    except:
        # Si hay algún error al obtener la comunidad, no es crítico
        pass
    
    context = {
        'username': username,
        'nombre': nombre,
        'community_name': community_name
    }
    
    return render(request, 'core/marketplace_home.html', context)


# Vistas para las noticias
def noticias(request):
    """
    Vista para mostrar el listado de noticias.
    
    Obtiene todas las noticias publicadas y las muestra paginadas,
    con la posibilidad de filtrar por búsqueda.
    """
    # Obtener parámetros de la URL
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    # Obtener todas las noticias publicadas ordenadas por fecha (más recientes primero)
    noticias_list = Noticia.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    
    # Aplicar filtro de búsqueda si existe
    if query:
        noticias_list = noticias_list.filter(
            Q(titulo__icontains=query) | 
            Q(resumen__icontains=query) | 
            Q(contenido__icontains=query)
        )
    
    # Configurar paginación - 9 artículos por página
    paginator = Paginator(noticias_list, 9)
    
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        noticias = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página
        noticias = paginator.page(paginator.num_pages)
    
    # Enriquecer los datos con información de los autores
    noticias_with_authors = []
    for noticia in noticias:
        try:
            autor = Usuario.objects.get(id=noticia.id_autor)
            autor_nombre = autor.nombre
            autor_apellido = autor.apellido
        except Usuario.DoesNotExist:
            autor_nombre = "Usuario"
            autor_apellido = "Desconocido"
        
        noticia.autor_nombre = autor_nombre
        noticia.autor_apellido = autor_apellido
    
    # Preparar datos para la plantilla
    context = {
        'noticias': noticias,
        'query': query,
        'current_page': int(page),
        'total_pages': paginator.num_pages,
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