# core/middleware.py
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages 
import logging

logger = logging.getLogger(__name__)

class AuthenticationMiddleware:
    """
    Middleware para controlar acceso a páginas protegidas.
    Solo usuarios logueados pueden acceder a las páginas internas.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs públicas que NO requieren autenticación
        self.public_urls = [
            '/login/',
            '/recovery/',
            '/register/',
            '/',  # Página de inicio
            '/admin/',  # Admin de Django
        ]
        
        # URLs que requieren autenticación (todas las demás)
        self.protected_patterns = [
            '/marketplace/',
            '/noticias/',
            '/eventos/',
            '/productos/',
            '/api/',
        ]

    def __call__(self, request):
        # Verificar si la URL actual está protegida
        if self.is_protected_url(request.path):
            # Verificar si el usuario está autenticado
            if not self.is_user_authenticated(request):
                logger.warning(f"Acceso no autorizado bloqueado: {request.path} desde IP {request.META.get('REMOTE_ADDR')}")
                
                # Si es una petición AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'Sesión expirada',
                        'redirect': reverse('core:login'),
                        'message': 'Debes iniciar sesión para acceder a esta página'
                    }, status=401)
                
                # Para peticiones normales, redirigir al login
                return redirect('core:login')
        
        # Procesar la petición normalmente
        response = self.get_response(request)
        return response
    
    def is_protected_url(self, path):
        """
        Determina si una URL requiere autenticación.
        """
        # Verificar si está en las URLs públicas
        for public_url in self.public_urls:
            if path.startswith(public_url):
                return False
        
        # Verificar si coincide con patrones protegidos
        for pattern in self.protected_patterns:
            if path.startswith(pattern):
                return True
        
        # URLs de archivos estáticos son públicas
        if path.startswith('/static/') or path.startswith('/media/'):
            return False
            
        # Por defecto, considerar protegida si no está explícitamente pública
        return True
    
    def is_user_authenticated(self, request):
        """
        Verifica si el usuario está autenticado basado en la sesión.
        """
        # Verificar que existe user_id en la sesión
        user_id = request.session.get('user_id')
        if not user_id:
            return False
        
        # Verificar que la sesión no haya expirado
        if request.session.get_expiry_age() <= 0:
            logger.info(f"Sesión expirada para usuario {user_id}")
            return False
        
        # Opcional: Verificar que el usuario existe en la base de datos
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM raiz.usuarios WHERE id = %s AND activo = true", 
                    [user_id]
                )
                user_exists = cursor.fetchone() is not None
                
            if not user_exists:
                logger.warning(f"Usuario {user_id} no encontrado o inactivo")
                request.session.flush()  # Limpiar sesión inválida
                return False
                
        except Exception as e:
            logger.error(f"Error verificando usuario en BD: {e}")
            # En caso de error de BD, mantener la sesión pero log el error
            pass
        
        return True


class SessionSecurityMiddleware:
    """
    Middleware adicional para seguridad de sesiones.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Regenerar session key periódicamente para seguridad
        if hasattr(request, 'session') and request.session.get('user_id'):
            # Verificar si la sesión es muy antigua (opcional)
            last_activity = request.session.get('last_activity')
            if last_activity:
                import time
                if time.time() - last_activity > 3600:  # 1 hora
                    request.session.cycle_key()
                    request.session['last_activity'] = time.time()
            else:
                request.session['last_activity'] = time.time()
        
        response = self.get_response(request)
        return response


class IPWhitelistMiddleware:
    """
    Middleware opcional para whitelist de IPs (para mayor seguridad).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # IPs permitidas (opcional - puedes comentar esto si no lo necesitas)
        self.allowed_ips = getattr(settings, 'ALLOWED_IPS', [])
    
    def __call__(self, request):
        # Solo aplicar whitelist si está configurado
        if self.allowed_ips:
            client_ip = self.get_client_ip(request)
            if client_ip not in self.allowed_ips:
                logger.warning(f"Acceso bloqueado desde IP no permitida: {client_ip}")
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Obtiene la IP real del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    





# core/middleware.py - AGREGAR ESTA CLASE

class EmailVerificationMiddleware:
    """
    Middleware para controlar acceso de usuarios no verificados
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que requieren verificación de email
        self.verification_required_patterns = [
            '/noticias/crear/',
            '/noticias/editar/',
            '/productos/',
            '/eventos/crear/',
        ]
        
        # URLs que NO requieren verificación (acceso básico)
        self.verification_exempt_patterns = [
            '/login/',
            '/logout/',
            '/register/',
            '/recovery/',
            '/verify-email/',
            '/marketplace/',
            '/noticias/',  # Ver noticias SÍ se permite
            '/api/',
        ]

    def __call__(self, request):
        # Solo aplicar a usuarios logueados
        if 'user_id' in request.session:
            # Verificar si el usuario está verificado
            user_verified = self.is_user_verified(request)
            
            # Si no está verificado y la URL requiere verificación
            if not user_verified and self.requires_verification(request.path):
                # Redirigir a página de verificación pendiente
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': 'Email no verificado',
                        'message': 'Debes verificar tu email antes de realizar esta acción',
                        'redirect': '/verify-email/'
                    }, status=403)
                
                messages.warning(request, 
                    'Debes verificar tu email antes de realizar esta acción. '
                    'Revisa tu bandeja de entrada.')
                return redirect('core:verify_email_pending')
        
        response = self.get_response(request)
        return response
    
    def is_user_verified(self, request):
        """Verifica si el usuario actual tiene email verificado"""
        try:
            user_id = request.session.get('user_id')
            from django.db import connection
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT verificado FROM raiz.usuarios WHERE id = %s",
                    [user_id]
                )
                result = cursor.fetchone()
                return result[0] if result else False
        except:
            return False
    
    def requires_verification(self, path):
        """Determina si una URL requiere verificación de email"""
        # Verificar URLs que requieren verificación
        for pattern in self.verification_required_patterns:
            if path.startswith(pattern):
                return True
        
        # Verificar URLs exentas
        for pattern in self.verification_exempt_patterns:
            if path.startswith(pattern):
                return False
        
        # Por defecto, no requerir verificación para otras URLs
        return False


# ==========================================
# VISTA PARA VERIFICACIÓN PENDIENTE
# ==========================================

def verify_email_pending(request):
    """Vista para mostrar página de verificación pendiente"""
    if 'user_id' not in request.session:
        return redirect('core:login')
    
    user_email = request.session.get('email', '')
    
    context = {
        'user_email': user_email,
        'user_name': request.session.get('nombre', 'Usuario')
    }
    
    return render(request, 'core/verify_email_pending.html', context)


# ==========================================
# VISTA PARA PROCESAR VERIFICACIÓN
# ==========================================

def verify_email(request, token):
    """Vista para procesar token de verificación"""
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Buscar usuario por token de verificación
            cursor.execute("""
                SELECT id, username, email, nombre 
                FROM raiz.usuarios 
                WHERE token_recuperacion = %s 
                AND verificado = false
                AND fecha_token > (CURRENT_TIMESTAMP - INTERVAL '24 HOURS')
            """, [token])
            
            user_data = cursor.fetchone()
            
            if user_data:
                user_id, username, email, nombre = user_data
                
                # Marcar como verificado
                cursor.execute("""
                    UPDATE raiz.usuarios 
                    SET verificado = true, 
                        token_recuperacion = NULL, 
                        fecha_token = NULL
                    WHERE id = %s
                """, [user_id])
                
                logger.info(f"Email verificado: {username} ({email})")
                
                # Mensaje de éxito
                messages.success(request, 
                    f'¡Email verificado correctamente! Bienvenido {nombre}. '
                    'Ahora puedes acceder a todas las funcionalidades.')
                
                return redirect('core:marketplace')
            else:
                # Token inválido o expirado
                messages.error(request, 
                    'El enlace de verificación es inválido o ha expirado. '
                    'Solicita un nuevo email de verificación.')
                
                return redirect('core:login')
                
    except Exception as e:
        logger.error(f"Error en verificación de email: {e}")
        messages.error(request, 'Error al verificar email.')
        return redirect('core:login')


# ==========================================
# FUNCIÓN PARA ENVIAR EMAIL DE VERIFICACIÓN
# ==========================================

def send_verification_email(user_id, email, username, nombre):
    """
    Envía email de verificación al usuario
    """
    import uuid
    import datetime
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.conf import settings
    
    try:
        # Generar token único
        verification_token = str(uuid.uuid4())
        
        # Guardar token en BD
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE raiz.usuarios 
                SET token_recuperacion = %s, 
                    fecha_token = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, [verification_token, user_id])
        
        # Crear enlace de verificación
        verification_url = f"{settings.SITE_URL}/verify-email/{verification_token}/"
        
        # Renderizar email HTML
        email_html = render_to_string('emails/verification_email.html', {
            'nombre': nombre,
            'username': username,
            'verification_url': verification_url,
        })
        
        # Enviar email
        send_mail(
            subject='Verifica tu cuenta en Raíz Digital',
            message=f'Hola {nombre}, verifica tu cuenta en: {verification_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=email_html,
            fail_silently=False,
        )
        
        logger.info(f"Email de verificación enviado a {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error enviando email de verificación: {e}")
        return False