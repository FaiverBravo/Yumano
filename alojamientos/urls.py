# alojamientos/urls.py
from django.urls import path
from . import views

app_name = 'alojamientos'  # Define el namespace para esta aplicación

urlpatterns = [
    # View for listing all alojamientos
    path('', views.alojamientos_list, name='Alojamientos'),
    
    # View for showing a single alojamiento detail
    path('<int:id>/', views.alojamiento_detalle, name='alojamiento_detalle'),
    
    # URL for reservation
    path('<int:id>/reservar/', views.reservar_alojamiento, name='reservar_alojamiento'),
    
    # URL for adding a post/comment
    path('<int:id>/comentario/', views.add_post, name='add_post'),

    path('procesar-imagenes/', views.procesar_imagenes, name='procesar_imagenes'),
    
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    
    path('alojamientos/', views.alojamientos_por_categoria, name='alojamientos'),
    
    path('categoria/<int:categoria_id>/', views.alojamientos_por_categoria, name='alojamientos_por_categoria'),
    
    path('subir-imagenes/', views.subir_imagenes_alojamiento, name='subir_imagenes_alojamiento'),

    path('imagenes/<int:id>/eliminar/', views.eliminar_imagen, name='eliminar_imagen'),
    
    path('gestionar-rapido/<int:id>/', views.gestionar_alojamiento_rapido, name='gestionar_alojamiento_rapido'),
]