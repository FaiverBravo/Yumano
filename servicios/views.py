from django.shortcuts import render, get_object_or_404

from servicios.models import Servicio

# Create your views here.

def servicios(request):
    servicios=Servicio.objects.all()
    return render(request, "servicios/servicios.html", {
        "servicios": servicios})

def servicio_detalle(request, id):
    item = get_object_or_404(Servicio, id=id)
    es_favorito = request.user.is_authenticated and item.favoritos.filter(usuario=request.user).exists()
    return render(request, "servicios/servicio_detalle.html", {"servicio": item, "es_favorito": es_favorito})
