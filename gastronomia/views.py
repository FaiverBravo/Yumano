from django.shortcuts import render, get_object_or_404

from gastronomia.models import Gastronomia

# Create your views here.

def gastronomia(request):
    gastronomia=Gastronomia.objects.all()
    return render(request, "gastronomia/gastronomia.html", {"gastronomia": gastronomia})

def gastronomia_detalle(request, id):
    item = get_object_or_404(Gastronomia, id=id)
    es_favorito = request.user.is_authenticated and item.favoritos.filter(usuario=request.user).exists()
    return render(request, "gastronomia/gastronomia_detalle.html", {"gastronomia": item, "es_favorito": es_favorito})