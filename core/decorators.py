# core/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def login_required_custom(view_func):
    """
    Decorador personalizado para requerir login.
    Más robusto que el decorador estándar de Django.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está logueado
        if not is_authenticated(request):
            # Log del intento de acceso no autorizado
            logger.warning(
                f"Acceso no autorizado a {request.path} desde IP {request.META.get('REMOTE_ADDR', 'unknown')}"
            )
            
            # Limpiar sesión inválida
            if hasattr(request, 'session'):
                request.session.flush()
            
            # Mensaje de error
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Sesión expirada',
                    'redirect': reverse('core:login'),
                    'message': 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
                }, status=401)
            
            # Redirigir al login
            return redirect('core:login')
        
        # Usuario autenticado, proceder con la vista
        return view_func(request, *args, **kwargs)
    
    return wrapper


def admin_required(view_func):
    """
    Decorador para requerir permisos de administrador.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Primero verificar autenticación
        if not is_authenticated(request):
            logger.warning(f"Acceso no autorizado a vista admin: {request.path}")
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('core:login')
        
        # Verificar permisos de admin
        if not is_admin_user(request):
            logger.warning(
                f"Usuario {request.session.get('username')} intentó acceder a vista admin: {request.path}"
            )
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('core:marketplace')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def ajax_login_required(view_func):
    """
    Decorador específico para vistas AJAX que requieren autenticación.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_authenticated(request):
            return JsonResponse({
                'error': 'Sesión expirada',
                'redirect': reverse('core:login'),
                'message': 'Tu sesión ha expirado'
            }, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def session_refresh(view_func):
    """
    Decorador para refrescar la sesión en cada petición autenticada.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if is_authenticated(request):
            # Extender la sesión
            request.session.set_expiry(3600)  # 1 hora
            request.session.modified = True
            
            # Actualizar último acceso
            import time
            request.session['last_activity'] = time.time()
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


# Funciones auxiliares
def is_authenticated(request):
    """
    Verifica si el usuario está autenticado de manera robusta.
    """
    # Verificar que existe sesión
    if not hasattr(request, 'session'):
        return False
    
    # Verificar user_id en sesión
    user_id = request.session.get('user_id')
    if not user_id:
        return False
    
    # Verificar que la sesión no ha expirado
    try:
        if request.session.get_expiry_age() <= 0:
            return False
    except:
        return False
    
    # Verificar usuario en base de datos (opcional, para mayor seguridad)
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM raiz.usuarios WHERE id = %s AND activo = true", 
                [user_id]
            )
            return cursor.fetchone() is not None
    except:
        # Si hay error en BD, mantener la sesión por ahora
        logger.warning(f"Error verificando usuario {user_id} en BD")
        return True


def is_admin_user(request):
    """
    Verifica si el usuario tiene permisos de administrador.
    """
    if not is_authenticated(request):
        return False
    
    # Verificar flag de admin en sesión
    is_admin = request.session.get('is_admin', False)
    if is_admin:
        return True
    
    # Si no está en sesión, verificar en BD
    try:
        user_id = request.session.get('user_id')
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM raiz.usuarios_roles ur
                JOIN raiz.roles r ON ur.id_rol = r.id
                WHERE ur.id_usuario = %s 
                AND r.nombre ILIKE %s
            """, [user_id, '%admin%'])
            
            is_admin = cursor.fetchone()[0] > 0
            
            # Guardar en sesión para futuras verificaciones
            request.session['is_admin'] = is_admin
            request.session.modified = True
            
            return is_admin
    except:
        logger.error(f"Error verificando permisos admin para usuario {request.session.get('user_id')}")
        return False


def get_user_info(request):
    """
    Obtiene información completa del usuario autenticado.
    """
    if not is_authenticated(request):
        return None
    
    return {
        'id': request.session.get('user_id'),
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'apellido': request.session.get('apellido'),
        'comunidad_id': request.session.get('comunidad_id'),
        'comunidad_nombre': request.session.get('comunidad_nombre'),
        'is_admin': is_admin_user(request)
    }