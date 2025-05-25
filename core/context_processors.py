# core/context_processors.py
from django.conf import settings

def media_url(request):
    """
    Context processor para hacer disponible MEDIA_URL en todas las plantillas
    """
    return {
        'MEDIA_URL': getattr(settings, 'MEDIA_URL', '/media/'),
        'STATIC_URL': getattr(settings, 'STATIC_URL', '/static/'),
    }