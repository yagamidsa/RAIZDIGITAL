from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
import os
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

     # Manejar favicon
    path('favicon.ico', RedirectView.as_view(
        url=settings.STATIC_URL + 'core/img/favicon.ico',
        permanent=True
    )),
]

# 🔧 CONFIGURACIÓN CORREGIDA PARA SERVIR ARCHIVOS MULTIMEDIA
if settings.DEBUG:
    # DESARROLLO: Django sirve archivos multimedia y estáticos
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print("🔧 Desarrollo: Django sirve archivos multimedia")
else:
    # PRODUCCIÓN: Configuración según el tipo de almacenamiento
    railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
    
    # Verificar si es el volumen de postgres (incorrecto) o no existe
    valid_volume = railway_volume and railway_volume != '/var/lib/postgresql/data'
    
    if valid_volume:
        # ✅ CON RAILWAY VOLUME CORRECTO: Servir archivos multimedia directamente
        print("💾 Producción: Archivos multimedia en Railway Volume (persistente)")
        print(f"📁 Volumen en: {railway_volume}")
        
        # Agregar ruta para servir archivos multimedia desde el volumen
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {
                'document_root': settings.MEDIA_ROOT,
            }),
        ]
        
    else:
        # ❌ SIN VOLUME O TEMPORAL: Los archivos están en staticfiles
        print("⚠️ Producción: Archivos multimedia temporales")
        print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"🔗 MEDIA_URL: {settings.MEDIA_URL}")
        
        # En este caso, WhiteNoise ya manejará los archivos como estáticos
        # No necesitamos rutas adicionales porque están en STATIC_ROOT
        if settings.MEDIA_URL.startswith('/static/'):
            print("📦 WhiteNoise manejará los archivos multimedia como estáticos")
        else:
            # Fallback: servir desde MEDIA_ROOT si es necesario
            urlpatterns += [
                re_path(r'^media/(?P<path>.*)$', serve, {
                    'document_root': settings.MEDIA_ROOT,
                }),
            ]

# 🔧 INFORMACIÓN DE DEBUG SOLO CUANDO CORRESPONDE
if settings.DEBUG:
    print(f"🌐 URLs configuradas para {'desarrollo' if settings.DEBUG else 'producción'}")
    print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"🔗 MEDIA_URL: {settings.MEDIA_URL}")
else:
    railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
    valid_volume = railway_volume and railway_volume != '/var/lib/postgresql/data'
    
    print(f"🌐 URLs configuradas para {'desarrollo' if settings.DEBUG else 'producción'}")
    print(f"💾 Volume válido: {'SÍ' if valid_volume else 'NO'}")
    print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"🔗 MEDIA_URL: {settings.MEDIA_URL}")

# Debug: Verificar rutas configuradas
print(f"🛣️ URLs totales configuradas: {len(urlpatterns)}")
for i, url_pattern in enumerate(urlpatterns):
    if hasattr(url_pattern, 'pattern'):
        print(f"   {i+1}. {url_pattern.pattern}")
    else:
        print(f"   {i+1}. {type(url_pattern).__name__}")