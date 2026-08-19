from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Usuario, Favorito
from .forms import RegistroForm, LoginForm, AlojamientoForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from alojamientos.models import Alojamiento, ImagenAlojamiento, Reserva
from tienda.models import Producto
from tienda.forms import ProductoForm
from gastronomia.models import Gastronomia
from experiencias.models import Experiencia
from servicios.models import Servicio
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from gastronomia.forms import GastronomiaForm
from experiencias.forms import ExperienciaForm
from servicios.forms import ServicioForm



def index(request):
    return render(request, "YumanoApp/index.html")

def nosotros(request):
    return render(request, "YumanoApp/nosotros.html")

def mapa(request):
    return render(request, "YumanoApp/mapa.html")

# registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Registro exitoso. ¡Bienvenido!")
                return redirect('dashboard_view')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
                print(f"Error al guardar: {str(e)}")
        else:
            # Muestra errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            print(form.errors)
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

# login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('dashboard_view')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


#------------------------------------------------
# dashboard
@login_required
def dashboard_view(request):
    tipo = request.user.tipo_usuario
    context = {
        'user': request.user,
        'title': 'Mi Panel',
    }
    
    # Lógica específica por tipo de usuario
    if tipo == 'anfitrion':
        from django.db.models import Avg
        alojamientos = Alojamiento.objects.filter(usuario=request.user)
        reservas = Reserva.objects.filter(alojamiento__usuario=request.user, estado='activa')
        
        # Calcular estadísticas reales
        total_resenas = sum([a.posts.count() for a in alojamientos])
        promedio = alojamientos.aggregate(promedio_total=Avg('posts__calificacion'))['promedio_total']
        
        alojamientos_con_imagenes = []
        for alojamiento in alojamientos:
            imagen_principal = alojamiento.imagenes.filter(es_principal=True).first()
            if not imagen_principal:
                imagen_principal = alojamiento.imagenes.first()
            todas_imagenes = list(alojamiento.imagenes.all())
            alojamientos_con_imagenes.append({
                'alojamiento': alojamiento,
                'imagen_principal': imagen_principal,
                'todas_imagenes': todas_imagenes,
            })
        
        mis_favoritos = Favorito.objects.filter(usuario=request.user)
        context.update({
            'title': 'Panel de Anfitrión',
            'alojamientos_count': alojamientos.count(),
            'reservas_activas': reservas.count(),
            'total_resenas': total_resenas,
            'calificacion_promedio': round(promedio, 1) if promedio else 0,
            'alojamientos_con_imagenes': alojamientos_con_imagenes,
            'reservas': reservas,
            'mis_favoritos': mis_favoritos,
        })
        template = 'YumanoApp/dashboard_anfitrion.html'
    
    elif tipo == 'turista' or tipo == 'cliente_local':
        mis_reservas = Reserva.objects.filter(usuario=request.user)
        mis_favoritos = Favorito.objects.filter(usuario=request.user)
        context.update({
            'title': 'Panel de Viajero',
            'mis_reservas': mis_reservas,
            'reservas_count': mis_reservas.count(),
            'mis_favoritos': mis_favoritos,
        })
        template = 'YumanoApp/dashboard_turista.html'
    
    elif tipo == 'admin':
        context.update({
            'title': 'Panel Administrativo',
            'dashboard_data': {
                'usuarios_totales': Usuario.objects.count(),
                'alojamientos_totales': Alojamiento.objects.count(),
                'reservas_totales': Reserva.objects.count(),
                'gastronomias_totales': Gastronomia.objects.count(),
                'productos_totales': Producto.objects.count(),
                'experiencias_totales': Experiencia.objects.count(),
                'servicios_totales': Servicio.objects.count(),
            }
        })
        template = 'YumanoApp/dashboard_admin.html'

    elif tipo in ['restaurantero', 'proveedor_experiencias', 'proveedor_servicios', 'vendedor']:
        # Vista unificada para vendedores (por ahora sin calificaciones complejas)
        if tipo == 'restaurantero':
            items = Gastronomia.objects.filter(usuario=request.user)
            form = GastronomiaForm()
        elif tipo == 'proveedor_experiencias':
            items = Experiencia.objects.filter(usuario=request.user)
            form = ExperienciaForm()
        elif tipo == 'proveedor_servicios':
            items = Servicio.objects.filter(usuario=request.user)
            form = ServicioForm()
        elif tipo == 'vendedor':
            items = Producto.objects.filter(usuario=request.user)
            form = ProductoForm()

        mis_favoritos = Favorito.objects.filter(usuario=request.user)
        context.update({
            'title': f'Panel de {request.user.get_tipo_usuario_display()}',
            'items': items,
            'items_count': items.count(),
            'form': form,
            'total_resenas': 0, # Placeholder para cuando se expandan reseñas a otros modelos
            'calificacion_promedio': 0,
            'mis_favoritos': mis_favoritos,
        })
        template = 'YumanoApp/dashboard_vendedor.html'

    else:
        # Fallback
        template = 'YumanoApp/dashboard_turista.html'
            
    return render(request, template, context)



# Vista de subida de imágenes
@login_required
def subir_imagenes_alojamiento(request):
    if request.method == 'POST':
        alojamiento_id = request.POST.get('alojamiento_id')
        try:
            alojamiento = Alojamiento.objects.get(id=alojamiento_id, usuario=request.user)
        except Alojamiento.DoesNotExist:
            messages.error(request, "No tienes permiso para editar este alojamiento.")
            return redirect('dashboard_view')

        imagenes = request.FILES.getlist('imagenes')
        ya_tiene_principal = alojamiento.imagenes.filter(es_principal=True).exists()

        for idx, imagen in enumerate(imagenes):
            es_principal = False
            if not ya_tiene_principal and idx == 0:
                es_principal = True
                ya_tiene_principal = True
            ImagenAlojamiento.objects.create(
                alojamiento=alojamiento,
                imagen=imagen,
                es_principal=es_principal
            )

        messages.success(request, "Imágenes subidas correctamente.")
        return redirect('dashboard_view')

    return redirect('dashboard_view')



@login_required
def subir_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario = request.user
            producto.save()
            messages.success(request, "Producto subido exitosamente.")
        else:
            messages.error(request, "Error al subir el producto.")
    return redirect('dashboard_view')

@login_required
def subir_gastronomia(request):
    if request.method == 'POST':
        form = GastronomiaForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()
            messages.success(request, "Plato/Servicio guardado exitosamente.")
    return redirect('dashboard_view')

@login_required
def subir_experiencia(request):
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()
            messages.success(request, "Experiencia guardada exitosamente.")
    return redirect('dashboard_view')

@login_required
def subir_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            obj.save()
            messages.success(request, "Servicio guardado exitosamente.")
    return redirect('dashboard_view')

@login_required
def editar_producto(request, pk):
    if request.user.tipo_usuario == 'admin':
        producto = get_object_or_404(Producto, pk=pk)
    else:
        producto = get_object_or_404(Producto, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('dashboard_view')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'YumanoApp/editar_producto.html', {'form': form, 'producto': producto, 'titulo_edicion': 'Editar Producto'})

@login_required
def eliminar_producto(request, pk):
    if request.user.tipo_usuario == 'admin':
        producto = get_object_or_404(Producto, pk=pk)
    else:
        producto = get_object_or_404(Producto, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
    return redirect('dashboard_view')


# Gastronomia
@login_required
def editar_gastronomia(request, pk):
    if request.user.tipo_usuario == 'admin':
        item = get_object_or_404(Gastronomia, pk=pk)
    else:
        item = get_object_or_404(Gastronomia, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        form = GastronomiaForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Plato/Servicio actualizado correctamente.")
            return redirect('dashboard_view')
    else:
        form = GastronomiaForm(instance=item)
    return render(request, 'YumanoApp/editar_producto.html', {'form': form, 'producto': item, 'titulo_edicion': 'Editar Gastronomía'})

@login_required
def eliminar_gastronomia(request, pk):
    if request.user.tipo_usuario == 'admin':
        item = get_object_or_404(Gastronomia, pk=pk)
    else:
        item = get_object_or_404(Gastronomia, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Plato/Servicio eliminado correctamente.")
    return redirect('dashboard_view')


# Experiencia
@login_required
def editar_experiencia(request, pk):
    if request.user.tipo_usuario == 'admin':
        item = get_object_or_404(Experiencia, pk=pk)
    else:
        item = get_object_or_404(Experiencia, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Experiencia actualizada correctamente.")
            return redirect('dashboard_view')
    else:
        form = ExperienciaForm(instance=item)
    return render(request, 'YumanoApp/editar_producto.html', {'form': form, 'producto': item, 'titulo_edicion': 'Editar Experiencia'})

@login_required
def eliminar_experiencia(request, pk):
    if request.user.tipo_usuario == 'admin':
        item = get_object_or_404(Experiencia, pk=pk)
    else:
        item = get_object_or_404(Experiencia, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Experiencia eliminada correctamente.")
    return redirect('dashboard_view')


# Servicio
@login_required
def editar_servicio(request, pk):
    if request.user.tipo_usuario == 'admin':
        item = get_object_or_404(Servicio, pk=pk)
    else:
        item = get_object_or_404(Servicio, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado correctamente.")
            return redirect('dashboard_view')
    else:
        form = ServicioForm(instance=item)
    return render(request, 'YumanoApp/editar_producto.html', {'form': form, 'producto': item, 'titulo_edicion': 'Editar Servicio'})

@login_required
def eliminar_servicio(request, pk):
    if request.user.tipo_usuario == 'admin':
        item = get_object_or_404(Servicio, pk=pk)
    else:
        item = get_object_or_404(Servicio, pk=pk, usuario=request.user)
        
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Servicio eliminado correctamente.")
    return redirect('dashboard_view')


# logout
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')


@login_required
def registrar_alojamiento(request):
    if request.method == 'POST':
        form = AlojamientoForm(request.POST, request.FILES)
        if form.is_valid():
            alojamiento = form.save(commit=False)
            alojamiento.usuario = request.user  # Asocia el alojamiento al usuario actual
            alojamiento.save()
            return redirect('dashboard_view')
    else:
        form = AlojamientoForm()
    return render(request, 'YumanoApp/registrar_alojamiento.html', {'form': form})

def api_map_data(request):
    data = {
        'alojamientos': [],
        'gastronomia': [],
        'experiencias': [],
        'servicios': [],
        'tienda': [],
    }
    
    # Alojamientos
    for obj in Alojamiento.objects.all():
        if obj.coordenadas:
            try:
                lat, lng = obj.coordenadas.split(',')
                # Obtener primera imagen
                img = obj.imagenes.first()
                img_url = img.imagen.url if img else None
                data['alojamientos'].append({
                    'id': obj.id,
                    'nombre': obj.nombre,
                    'lat': float(lat.strip()),
                    'lng': float(lng.strip()),
                    'descripcion': obj.descripcion[:100] + '...',
                    'imagen': img_url,
                    'url': f'/alojamientos/{obj.id}/'
                })
            except: pass

    # Gastronomía
    for obj in Gastronomia.objects.all():
        if obj.coordenadas:
            try:
                lat, lng = obj.coordenadas.split(',')
                data['gastronomia'].append({
                    'id': obj.id,
                    'nombre': obj.nombre,
                    'lat': float(lat.strip()),
                    'lng': float(lng.strip()),
                    'descripcion': obj.descripcion[:100] + '...',
                    'imagen': obj.imagen.url if obj.imagen else None,
                    'url': '#'
                })
            except: pass

    # Experiencias
    for obj in Experiencia.objects.all():
        if obj.coordenadas:
            try:
                lat, lng = obj.coordenadas.split(',')
                data['experiencias'].append({
                    'id': obj.id,
                    'nombre': obj.nombre,
                    'lat': float(lat.strip()),
                    'lng': float(lng.strip()),
                    'descripcion': obj.descripcion[:100] + '...',
                    'imagen': obj.imagen.url if obj.imagen else None,
                    'url': '#'
                })
            except: pass

    # Servicios
    for obj in Servicio.objects.all():
        if obj.coordenadas:
            try:
                lat, lng = obj.coordenadas.split(',')
                data['servicios'].append({
                    'id': obj.id,
                    'nombre': obj.nombre,
                    'lat': float(lat.strip()),
                    'lng': float(lng.strip()),
                    'descripcion': obj.descripcion[:100] + '...',
                    'imagen': obj.imagen.url if obj.imagen else None,
                    'url': '#'
                })
            except: pass

    return JsonResponse(data)


@login_required
@require_POST
def toggle_favorito(request):
    tipo = request.POST.get('tipo')
    item_id = request.POST.get('id')
    
    if not tipo or not item_id:
        return JsonResponse({'status': 'error', 'message': 'Faltan parámetros'}, status=400)
    
    params = {'usuario': request.user}
    if tipo == 'alojamiento':
        params['alojamiento_id'] = item_id
    elif tipo == 'gastronomia':
        params['gastronomia_id'] = item_id
    elif tipo == 'experiencia':
        params['experiencia_id'] = item_id
    elif tipo == 'servicio':
        params['servicio_id'] = item_id
    elif tipo == 'producto':
        params['producto_id'] = item_id
    else:
        return JsonResponse({'status': 'error', 'message': 'Tipo no válido'}, status=400)
        
    fav, created = Favorito.objects.get_or_create(**params)
    if not created:
        fav.delete()
        active = False
    else:
        active = True
        
    return JsonResponse({'status': 'success', 'active': active})

@login_required
@require_POST
def toggle_disponibilidad(request):
    tipo = request.POST.get('tipo')
    item_id = request.POST.get('id')
    
    if not tipo or not item_id:
        return JsonResponse({'status': 'error', 'message': 'Faltan parámetros'}, status=400)
    
    # Validar permisos (solo el propietario puede cambiar la disponibilidad)
    try:
        active = False
        if tipo == 'alojamiento':
            item = Alojamiento.objects.get(id=item_id, usuario=request.user)
            item.disponibilidad = not item.disponibilidad
            item.save()
            active = item.disponibilidad
        elif tipo == 'producto':
            item = Producto.objects.get(id=item_id, usuario=request.user)
            item.disponibilidad = not item.disponibilidad
            item.save()
            active = item.disponibilidad
        elif tipo == 'experiencia':
            item = Experiencia.objects.get(id=item_id, usuario=request.user)
            item.disponibilidad = not item.disponibilidad
            item.save()
            active = item.disponibilidad
        else:
            return JsonResponse({'status': 'error', 'message': 'Tipo no válido'}, status=400)
            
        return JsonResponse({'status': 'success', 'active': active})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'No tienes permiso o el ítem no existe'}, status=403)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        foto = request.FILES.get('foto_perfil')
        
        user = request.user
        if nombre:
            user.nombre = nombre
        if apellido:
            user.apellido = apellido
        if email:
            user.email = email
        if telefono is not None:
            user.telefono = telefono
        if foto:
            user.foto_perfil = foto
            
        user.save()
        messages.success(request, "Perfil actualizado exitosamente.")
    return redirect('dashboard_view')


from django.urls import reverse
from django.db.models import Q

def api_search(request):
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'all').strip()
    
    results = {
        'alojamientos': [],
        'experiencias': [],
        'gastronomia': [],
        'tienda': [],
        'servicios': []
    }
    
    if len(query) < 2:
        return JsonResponse(results)
        
    def serialize_item(item, category, url_name):
        img_url = ''
        if hasattr(item, 'imagen') and item.imagen:
            try:
                img_url = item.imagen.url
            except ValueError:
                pass
        elif hasattr(item, 'imagenes'):
            img_obj = item.imagenes.filter(es_principal=True).first() or item.imagenes.first()
            if img_obj and img_obj.imagen:
                try:
                    img_url = img_obj.imagen.url
                except ValueError:
                    pass
        
        desc = item.descripcion if hasattr(item, 'descripcion') else ''
        if desc and len(desc) > 100:
            desc = desc[:97] + '...'
            
        try:
            item_url = reverse(url_name, args=[item.id])
        except Exception:
            item_url = '#'
            
        return {
            'id': item.id,
            'nombre': item.nombre,
            'descripcion': desc,
            'precio': str(item.precio) if getattr(item, 'precio', None) is not None else None,
            'imagen': img_url,
            'url': item_url
        }

    q_filter = Q(nombre__icontains=query) | Q(descripcion__icontains=query)

    if search_type in ('all', 'alojamientos'):
        alojamientos = Alojamiento.objects.filter(q_filter)[:5]
        results['alojamientos'] = [serialize_item(x, 'alojamientos', 'alojamientos:alojamiento_detalle') for x in alojamientos]

    if search_type in ('all', 'experiencias'):
        experiencias = Experiencia.objects.filter(q_filter)[:5]
        results['experiencias'] = [serialize_item(x, 'experiencias', 'experiencias:experiencia_detalle') for x in experiencias]

    if search_type in ('all', 'gastronomia'):
        gastronomia = Gastronomia.objects.filter(q_filter)[:5]
        results['gastronomia'] = [serialize_item(x, 'gastronomia', 'gastronomia:gastronomia_detalle') for x in gastronomia]

    if search_type in ('all', 'tienda'):
        productos = Producto.objects.filter(q_filter)[:5]
        results['tienda'] = [serialize_item(x, 'tienda', 'tienda:producto_detalle') for x in productos]

    if search_type in ('all', 'servicios'):
        servicios = Servicio.objects.filter(q_filter)[:5]
        results['servicios'] = [serialize_item(x, 'servicios', 'servicios:servicio_detalle') for x in servicios]

    return JsonResponse(results)