"""
URL configuration for raizdigital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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

# 🔧 CONFIGURACIÓN PARA SERVIR ARCHIVOS MULTIMEDIA
if settings.DEBUG:
    # DESARROLLO: Django sirve archivos multimedia
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print("🔧 Desarrollo: Django sirve multimedia")
else:
    # PRODUCCIÓN: Verificar si hay Railway Volume
    railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
    
    if railway_volume:
        # ✅ CON RAILWAY VOLUME: WhiteNoise sirve desde el volumen persistente
        print("💾 Producción: WhiteNoise + Railway Volume (persistente)")
        # WhiteNoise manejará todo automáticamente gracias a STATICFILES_DIRS
    else:
        # ❌ SIN VOLUME: Ruta explícita para archivos temporales
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {
                'document_root': settings.STATIC_ROOT / 'media',
            }),
        ]
        print("⚠️ Producción: Almacenamiento temporal")

print(f"🌐 URLs configuradas para {'desarrollo' if settings.DEBUG else 'producción'}")
print(f"💾 Volume: {'SÍ' if os.environ.get('RAILWAY_VOLUME_MOUNT_PATH') else 'NO'}")