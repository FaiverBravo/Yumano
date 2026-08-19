from django.urls import path
from .views import contacto

app_name = 'contacto'


urlpatterns = [
    
    path('', contacto, name='Contacto'),
    
]
