from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('recovery/', views.password_recovery, name='password_recovery'),
    path('register/', views.register, name='register'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/crear/', views.crear_noticia, name='crear_noticia'),
    path('noticias/editar/<slug:slug>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/<slug:slug>/', views.noticia_detalle, name='noticia_detalle'),
    path('noticias/like/<str:noticia_id>/', views.like_noticia, name='like_noticia'),
]