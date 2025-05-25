from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# 🔧 CONFIGURACIÓN CORREGIDA PARA SERVIR ARCHIVOS MULTIMEDIA
if settings.DEBUG:
    # DESARROLLO: Django sirve archivos multimedia
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print("🔧 Desarrollo: Django sirve multimedia")
else:
    # PRODUCCIÓN: Configuración según el tipo de almacenamiento
    railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
    
    # Verificar si es el volumen de postgres (incorrecto)
    if railway_volume == '/var/lib/postgresql/data':
        railway_volume = None
        print("⚠️ Volumen de Postgres detectado - usando almacenamiento temporal")
    
    if railway_volume and railway_volume != '/var/lib/postgresql/data':
        # ✅ CON RAILWAY VOLUME CORRECTO: WhiteNoise maneja todo
        print("💾 Producción: WhiteNoise + Railway Volume (persistente)")
        print(f"📁 Volumen en: {railway_volume}")
        
        # Agregar ruta explícita para multimedia si es necesario
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {
                'document_root': settings.MEDIA_ROOT,
            }),
        ]
        
    else:
        # ❌ SIN VOLUME O TEMPORAL: Ruta explícita desde archivos estáticos
        print("⚠️ Producción: Almacenamiento temporal en static/media/")
        
        # Media se sirve como archivos estáticos
        urlpatterns += [
            re_path(r'^static/media/(?P<path>.*)$', serve, {
                'document_root': settings.MEDIA_ROOT,
            }),
        ]

print(f"🌐 URLs configuradas para {'desarrollo' if settings.DEBUG else 'producción'}")
print(f"💾 Volume válido: {'SÍ' if railway_volume and railway_volume != '/var/lib/postgresql/data' else 'NO'}")
print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"🔗 MEDIA_URL: {settings.MEDIA_URL}")