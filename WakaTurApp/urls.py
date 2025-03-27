from django.urls import path
from .views import index, nosotros, mapa, registro, user_login, user_logout, dashboard_view, tu_funcion_vista

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
    

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="WakaTurApp/registration/password_reset.html"), 
        name="password_reset"
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="WakaTurApp/registration/password_reset_done.html"), 
        name="password_reset_done"
    ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="WakaTurApp/registration/password_reset_confirm.html"), 
        name="password_reset_confirm"
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="WakaTurApp/registration/password_reset_complete.html"), 
        name="password_reset_complete"
    ),
    path('ruta/a/tu/vista/', tu_funcion_vista, name='tu_vista_para_procesar'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)