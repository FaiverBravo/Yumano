from django.urls import path
from .views import (
    index, nosotros, mapa, registro, user_login, user_logout, dashboard_view,
    registrar_alojamiento, subir_producto, editar_producto, eliminar_producto,
    api_map_data, subir_gastronomia, subir_experiencia, subir_servicio,
    toggle_favorito, editar_perfil,
    editar_gastronomia, eliminar_gastronomia,
    editar_experiencia, eliminar_experiencia,
    editar_servicio, eliminar_servicio,
    toggle_disponibilidad, api_search
)
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='Inicio'),
    path('nosotros/', nosotros, name='Nosotros'),
    path('mapa/', mapa, name='Mapa'),
    path('registro/', registro, name='registro'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard_view/', dashboard_view, name='dashboard_view'),
    path('registrar-alojamiento/', registrar_alojamiento, name='registrar_alojamiento'),
    path('subir-producto/', subir_producto, name='subir_producto'),
    path('editar-producto/<int:pk>/', editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:pk>/', eliminar_producto, name='eliminar_producto'),

    # Gastronomia Edit/Delete
    path('editar-gastronomia/<int:pk>/', editar_gastronomia, name='editar_gastronomia'),
    path('eliminar-gastronomia/<int:pk>/', eliminar_gastronomia, name='eliminar_gastronomia'),

    # Experiencia Edit/Delete
    path('editar-experiencia/<int:pk>/', editar_experiencia, name='editar_experiencia'),
    path('eliminar-experiencia/<int:pk>/', eliminar_experiencia, name='eliminar_experiencia'),

    # Servicio Edit/Delete
    path('editar-servicio/<int:pk>/', editar_servicio, name='editar_servicio'),
    path('eliminar-servicio/<int:pk>/', eliminar_servicio, name='eliminar_servicio'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"), 
        name="password_reset"
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"), 
        name="password_reset_done"
    ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"), 
        name="password_reset_confirm"
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"), 
        name="password_reset_complete"
    ),
    path('api/map-data/', api_map_data, name='api_map_data'),
    path('subir-gastronomia/', subir_gastronomia, name='subir_gastronomia'),
    path('subir-experiencia/', subir_experiencia, name='subir_experiencia'),
    path('subir-servicio/', subir_servicio, name='subir_servicio'),
    path('toggle-favorito/', toggle_favorito, name='toggle_favorito'),
    path('toggle-disponibilidad/', toggle_disponibilidad, name='toggle_disponibilidad'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('api/search/', api_search, name='api_search'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)