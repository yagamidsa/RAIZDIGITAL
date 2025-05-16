from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('core:index')  # O redirige a donde prefieras después del login
        else:
            return render(request, 'core/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'core/login.html')


def password_recovery(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Verificar si el email existe en la base de datos
        try:
            user = User.objects.get(email=email)
            
            # En un entorno real, aquí generarías un token único para la recuperación
            # y lo enviarías por correo electrónico con un enlace para restablecer la contraseña
            
            # Como es una demostración, simplemente mostramos un mensaje de éxito
            context = {
                'success': 'Hemos enviado las instrucciones para restablecer tu contraseña a tu correo electrónico.'
            }
            return render(request, 'core/password_recovery.html', context)
            
        except User.DoesNotExist:
            # Si el correo no existe, mostramos un mensaje genérico por seguridad
            # No informamos que el correo no existe para evitar enumeración de usuarios
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
    return render(request, 'core/marketplace_home.html')


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