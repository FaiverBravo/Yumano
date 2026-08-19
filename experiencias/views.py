from django.shortcuts import render, get_object_or_404

from experiencias.models import Experiencia

# Create your views here.

def experiencias(request):
    experiencias=Experiencia.objects.all()
    return render(request, "experiencias/experiencias.html", {"experiencias": experiencias})

def experiencia_detalle(request, id):
    experiencia = get_object_or_404(Experiencia, id=id)
    es_favorito = request.user.is_authenticated and experiencia.favoritos.filter(usuario=request.user).exists()
    return render(request, "experiencias/experiencia_detalle.html", {"experiencia": experiencia, "es_favorito": es_favorito})

