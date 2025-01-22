"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),  # Registro de usuarios
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),  # Inicio de sesión
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),  # Cierre de sesión
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #path('inicio/', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('mueble/<int:mueble_id>/', views.detalle_mueble, name='detalle_mueble'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
