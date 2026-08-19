from django.shortcuts import render, get_object_or_404
from .models import Producto

# Create your views here.

def tienda(request):

    productos=Producto.objects.all()

    return render(request, "tienda/tienda.html", {"productos":productos})

def producto_detalle(request, id):
    item = get_object_or_404(Producto, id=id)
    es_favorito = request.user.is_authenticated and item.favoritos.filter(usuario=request.user).exists()
    return render(request, "tienda/producto_detalle.html", {"producto": item, "es_favorito": es_favorito})
