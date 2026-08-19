from django.urls import path
from . import views

app_name = 'servicios'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('',views.servicios, name='Servicios'),
    path('<int:id>/', views.servicio_detalle, name='servicio_detalle'),
    

]