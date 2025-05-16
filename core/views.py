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

@login_required
def marketplace(request):
    return render(request, 'core/marketplace.html')

def marketplace(request):
    context = {
        'comunidades': [
            {
                'nombre': 'Wayúu',
                'region': 'La Guajira',
                'pais': 'Colombia',
                'imagen': 'wayuu.jpg',
                'descripcion': 'Comunidad indígena reconocida por sus tejidos y mochilas tradicionales.'
            },
            {
                'nombre': 'Embera',
                'region': 'Chocó',
                'pais': 'Colombia',
                'imagen': 'embera.jpg',
                'descripcion': 'Conocidos por su artesanía en chaquira y cestería tradicional.'
            },
            {
                'nombre': 'Arhuaco',
                'region': 'Sierra Nevada',
                'pais': 'Colombia',
                'imagen': 'arhuaco.jpg',
                'descripcion': 'Tejedores de mochilas con diseños que representan su cosmovisión.'
            }
        ],
        'productos': [
            {
                'nombre': 'Mochila Wayúu',
                'descripcion': 'Tejido a mano por artesanas Wayúu',
                'precio': 150000,
                'descuento': 10,
                'precio_original': 167000,
                'precio_actual': 150000,
                'imagen': 'mochila_wayuu.jpg',
                'categoria': 'Textiles',
                'comunidad': 'Wayúu',
                'calificacion': 4.8,
                'num_resenas': 24,
                'vendedor': 'María Pushaina',
                'es_nuevo': True
            },
            # Añade más productos...
        ],
        'artesanos': [
            {
                'nombre': 'María',
                'apellido': 'Pushaina',
                'foto': 'maria_pushaina.jpg',
                'comunidad': 'Wayúu',
                'especialidad': 'Tejido tradicional',
                'productos': 23,
                'ventas': 142,
                'calificacion': 4.9
            },
            # Añade más artesanos...
        ],
        'noticias': [
            {
                'titulo': 'Festival de Cultura Indígena 2023',
                'resumen': 'El festival anual celebrará la diversidad cultural de las comunidades indígenas de Colombia.',
                'imagen': 'festival.jpg',
                'fecha': '2023-09-15',
                'autor': 'Juan Carlos Rodríguez',
                'categoria': 'Eventos'
            },
            # Añade más noticias...
        ],
        'eventos': [
            {
                'titulo': 'Taller de Tejido Wayúu',
                'descripcion': 'Aprende las técnicas ancestrales de tejido Wayúu de la mano de artesanas tradicionales.',
                'fecha': '2023-08-25',
                'hora': '10:00 AM',
                'ubicacion': 'Centro Cultural La Candelaria, Bogotá',
                'comunidad': 'Wayúu'
            },
            # Añade más eventos...
        ]
    }
    return render(request, 'core/marketplace_home.html', context)


