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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# 🔧 CONFIGURACIÓN MEJORADA PARA SERVIR ARCHIVOS
if settings.DEBUG:
    # DESARROLLO: Servir archivos multimedia normalmente
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print("🔧 Configuración de desarrollo: Django sirve archivos multimedia")
else:
    # 🔧 PRODUCCIÓN: WhiteNoise sirve todo, pero agregamos ruta explícita por si acaso
    try:
        # Ruta explícita para archivos multimedia en producción
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {
                'document_root': settings.STATIC_ROOT / 'media',
            }),
        ]
        print("📦 Configuración de producción: WhiteNoise + ruta explícita para multimedia")
    except Exception as e:
        print(f"⚠️ Error configurando multimedia en producción: {e}")

print(f"🌐 URLs configuradas para {'desarrollo' if settings.DEBUG else 'producción'}")