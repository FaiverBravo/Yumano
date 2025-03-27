# alojamientos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alojamiento, Post, ImagenAlojamiento, Categoria, Reserva
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator
from .forms import AlojamientoForm


# vista alojamientos
def alojamientos_list(request):
    # Obtener todas las categorías para mostrarlas como filtros
    categorias = Categoria.objects.all()

    # Obtener los alojamientos, aplicando filtros si es necesario
    alojamientos = Alojamiento.objects.all()

    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        alojamientos = alojamientos.filter(categorias__id=categoria_id)

    # Filtro por búsqueda
    query = request.GET.get('q')
    if query:
        alojamientos = alojamientos.filter(nombre__icontains=query)

    
    # Paginación
    paginator = Paginator(alojamientos, 6)  # Mostrar 6 alojamientos por página
    page_number = request.GET.get('page')
    alojamientos = paginator.get_page(page_number)

    context = {
        'categorias': categorias,
        'alojamientos': alojamientos,
    }
    return render(request, 'alojamientos/alojamientos.html', context)

# Vista para el detalle de un alojamiento
def alojamiento_detalle(request, id):
    alojamiento = get_object_or_404(Alojamiento, id=id)
    principal_img = alojamiento.imagenes.filter(es_principal=True).first()  # Obtener la imagen principal
    context = {
        'alojamiento': alojamiento,
        'principal_img': principal_img,
    }
    return render(request, 'alojamientos/alojamiento_detalle.html', context)


# Vista para subir imágenes de alojamientos
def subir_imagenes_alojamiento(request):
    if request.method == 'POST':
        alojamiento_id = request.POST.get('alojamiento_id')
        
        # Verificar que el alojamiento_id no esté vacío
        if not alojamiento_id:
            messages.error(request, "Debes seleccionar un alojamiento.")
            return redirect('alojamientos:lista_alojamientos')

        # Obtener el alojamiento o devolver un error 404 si no existe
        alojamiento = get_object_or_404(Alojamiento, id=alojamiento_id)

        # Procesar las imágenes
        imagenes = request.FILES.getlist('imagenes')
        if not imagenes:
            messages.error(request, "Debes seleccionar al menos una imagen.")
            return redirect('alojamientos:lista_alojamientos')

        for imagen in imagenes:
            ImagenAlojamiento.objects.create(alojamiento=alojamiento, imagen=imagen)

        messages.success(request, f"Se han subido {len(imagenes)} imágenes al alojamiento {alojamiento.nombre}.")
        return redirect('alojamientos:alojamiento_detalle', id=alojamiento.id)

    return redirect('alojamientos:lista_alojamientos')


# Vista para procesar imágenes de alojamientos
@login_required
def procesar_imagenes(request):
    alojamiento_id = request.GET.get('alojamiento_id') or request.POST.get('alojamiento_id')
    
    # Si es GET con ID, redirigir a la página de detalles con el formulario
    if request.method == 'GET' and alojamiento_id:
        return redirect('alojamientos:alojamiento_detalle', alojamiento_id=alojamiento_id)
    
    if request.method == 'POST':
        imagenes = request.FILES.getlist('imagenes')
        es_principal = request.POST.get('es_principal')
        alojamiento_id = request.POST.get('alojamiento_id')
        
        if not alojamiento_id or not imagenes:
            messages.error(request, "Debes seleccionar un alojamiento y al menos una imagen")
            return redirect('dashboard_view')
        
        try:
            alojamiento = Alojamiento.objects.get(id=alojamiento_id, propietario=request.user)
            
            # Si se marca como principal, quitar el estado de principal de otras imágenes
            if es_principal:
                ImagenAlojamiento.objects.filter(alojamiento=alojamiento, es_principal=True).update(es_principal=False)
            
            # Procesar cada imagen
            for imagen in imagenes:
                nueva_imagen = ImagenAlojamiento(
                    alojamiento=alojamiento,
                    imagen=imagen,
                    es_principal=(imagen.name == es_principal)
                )
                nueva_imagen.save()
            
            messages.success(request, f"Se han subido {len(imagenes)} imágenes al alojamiento {alojamiento.nombre}")
            return redirect('alojamientos:alojamiento_detalle', alojamiento_id=alojamiento.id)
            
        except Alojamiento.DoesNotExist:
            messages.error(request, "El alojamiento seleccionado no existe o no tienes permisos para modificarlo")
        except Exception as e:
            messages.error(request, f"Error al procesar imágenes: {str(e)}")
    
    return redirect('dashboard_view')

# Eliminar imagenes de alojamiento

@login_required
def eliminar_imagen(request, id):
    imagen = get_object_or_404(ImagenAlojamiento, id=id, alojamiento__usuario=request.user)
    if request.method == 'POST':
        imagen.delete()
        messages.success(request, "La imagen ha sido eliminada con éxito.")
        return redirect('alojamientos:listar_imagenes')
    return render(request, 'alojamientos/eliminar_imagen.html', {'imagen': imagen})

# Vista para listar imagenes de alojamiento

# Vista para reservar alojamiento
@login_required
def reservar_alojamiento(request, id):
    alojamiento = get_object_or_404(Alojamiento, id=id)
    
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        num_personas = int(request.POST.get('num_personas'))

        if not fecha_inicio or not fecha_fin:
            messages.error(request, "Debes proporcionar las fechas de inicio y fin.")
            return redirect('alojamientos:alojamiento_detalle', id=alojamiento.id)

        # Calcular el número de días de la estadía
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            dias_estadia = (fecha_fin_dt - fecha_inicio_dt).days
        except ValueError:
            messages.error(request, "Las fechas proporcionadas no son válidas.")
            return redirect('alojamientos:alojamiento_detalle', id=alojamiento.id)

        if dias_estadia <= 0:
            messages.error(request, "La fecha de fin debe ser posterior a la fecha de inicio.")
            return redirect('alojamientos:alojamiento_detalle', id=alojamiento.id)

        # Calcular el precio total
        precio_unitario = alojamiento.precio
        precio_total = dias_estadia * precio_unitario * num_personas

        # Crear la reserva
        Reserva.objects.create(
            alojamiento=alojamiento,
            usuario=request.user,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            num_personas=num_personas,
            precio_unitario=precio_unitario,
            precio_total=precio_total,
            estado='activa'
            
        )
      
        messages.success(request, f"Reserva realizada con éxito para {alojamiento.nombre}.")
        return redirect('alojamientos:alojamiento_detalle', id=alojamiento.id)

    return redirect('alojamientos:alojamiento_detalle', id=alojamiento.id)




# Vista para agregar un post a un alojamiento
def add_post(request, id):
    alojamiento = get_object_or_404(Alojamiento, id=id)
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        if descripcion:
            Post.objects.create(
                alojamiento=alojamiento,
                autor=request.user,  # Assuming you're using Django's authentication
                descripcion=descripcion
            )
    return redirect('alojamientos:alojamiento_detalle', id=id)

# View to list all categories 

def lista_categorias(request):
    # Obtener todas las categorías
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Opcional: obtener conteo de alojamientos por categoría
    for categoria in categorias:
        categoria.num_alojamientos = categoria.alojamientos.count()
    
    context = {
        'categorias': categorias,
    }
    
    # Usando una ruta más específica para la plantilla
    return render(request, 'alojamientos/categorias.html', context)


# Para filtrar alojamientos por categoría

def alojamientos_por_categoria(request, categoria_id=None):
    # Obtener todas las categorías para el menú de filtro
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Filtrar alojamientos por categoría si se proporciona
    if categoria_id:
        categoria = Categoria.objects.get(id=categoria_id)
        # Si hay relación ManyToMany, usar esto:
        alojamientos = categoria.alojamientos.all()
    else:
        alojamientos = Alojamiento.objects.all()
    
    context = {
        'categorias': categorias,
        'alojamientos': alojamientos,
        'categoria_actual': categoria_id,
    }
    
    return render(request, 'alojamientos.html', context)


# Crear un nuevo alojamiento
def crear_alojamiento(request):
    if request.method == 'POST':
        form = AlojamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alojamientos:lista_alojamientos')
    else:
        form = AlojamientoForm()
    return render(request, 'alojamientos/crear_alojamiento.html', {'form': form})

# Editar un alojamiento existente
def editar_alojamiento(request, id):
    alojamiento = get_object_or_404(Alojamiento, id=id)
    if request.method == 'POST':
        form = AlojamientoForm(request.POST, instance=alojamiento)
        if form.is_valid():
            form.save()
            return redirect('alojamientos:detalle_alojamiento', id=alojamiento.id)
    else:
        form = AlojamientoForm(instance=alojamiento)
    return render(request, 'alojamientos/editar_alojamiento.html', {'form': form})

