from django.urls import path
from . import views

app_name = 'tienda'


urlpatterns = [
   
    
    path('',views.tienda, name='Tienda'),
    path('<int:id>/', views.producto_detalle, name='producto_detalle'),
    

]