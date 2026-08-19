from django.urls import path
from . import views

app_name = 'gastronomia'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('',views.gastronomia, name='Gastronomia'),
    path('<int:id>/', views.gastronomia_detalle, name='gastronomia_detalle'),
    

]