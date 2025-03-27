from django.urls import path
from .views import contacto


urlpatterns = [
    
    path('', contacto, name='Contacto'),
    
]
