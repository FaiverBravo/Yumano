from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),

    # Enlace de urls entre proyecto principal con App YumanoApp
    path('', include('YumanoApp.urls')),    
    path('alojamientos/', include('alojamientos.urls', namespace='alojamientos')),
    path('experiencias/', include('experiencias.urls', namespace='experiencias')),
    path('gastronomia/', include('gastronomia.urls', namespace='gastronomia')),
    path('servicios/', include('servicios.urls', namespace='servicios')),
    path('tienda/', include('tienda.urls', namespace='tienda')),
    path('contacto/', include('contacto.urls', namespace='contacto')),
    path('accounts/', include('django.contrib.auth.urls')),

    
   
]

 # Add this if you're using Django to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)