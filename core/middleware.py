# core/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
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