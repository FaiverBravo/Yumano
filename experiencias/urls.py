from django.urls import path
from . import views

app_name = 'experiencias'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('',views.experiencias, name='Experiencias'),
    path('<int:id>/', views.experiencia_detalle, name='experiencia_detalle'),
    

]