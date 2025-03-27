from re import template
from unicodedata import name
from django.contrib import  admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),

    #enlace de urls entre Proyecto principal con App WakaTurApp
    path('', include('WakaTurApp.urls')),    
    path('alojamientos/', include('alojamientos.urls', namespace='alojamientos')),
    path('experiencias/', include('experiencias.urls')),
    path('gastronomia/', include('gastronomia.urls')),
    path('servicios/', include('servicios.urls')),
    path('tienda/', include('tienda.urls')),
    path('contacto/', include('contacto.urls')),    
    path('WakaTurApp/', include('django.contrib.auth.urls')), 
    path('WakaTurApp/', include('WakaTurApp.urls')), 

    
   
]

 # Add this if you're using Django to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)