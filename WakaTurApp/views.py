from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistroForm, LoginForm, AlojamientoForm
from django.contrib import messages
from alojamientos.models import Alojamiento, ImagenAlojamiento, Reserva
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "WakaTurApp/index.html")

def nosotros(request):
    return render(request, "WakaTurApp/nosotros.html")

def mapa(request):
    return render(request, "WakaTurApp/mapa.html")

# registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Registro exitoso. ¡Bienvenido!")
                return redirect('login')
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
    alojamientos = Alojamiento.objects.filter(usuario=request.user)
    reservas = Reserva.objects.filter(usuario=request.user, estado='activa')

    dashboard_data = {
        'alojamientos': alojamientos.count(),
        'reservas': reservas.count(),
    }

    alojamientos_con_imagenes = []
    for alojamiento in alojamientos:
        imagen_principal = alojamiento.imagenes.filter(es_principal=True).first()
        if not imagen_principal:
            imagen_principal = alojamiento.imagenes.first()
        alojamientos_con_imagenes.append({
            'alojamiento': alojamiento,
            'imagen_principal': imagen_principal,
        })

    context = {
        'title': 'Dashboard Anfitrión',
        'user': request.user,
        'dashboard_data': dashboard_data,
        'alojamientos_con_imagenes': alojamientos_con_imagenes,
        'reservas': reservas,
    }
    return render(request, 'WakaTurApp/dashboard_anfitrion.html', context)



# 
def subir_imagenes_alojamiento(request):
    if request.method == 'POST':
        alojamiento_id = request.POST.get('alojamiento_id')
        alojamiento = Alojamiento.objects.get(id=alojamiento_id)

        for imagen in request.FILES.getlist('imagenes'):
            nueva_imagen = ImagenAlojamiento.objects.create(alojamiento=alojamiento, imagen=imagen)
            nueva_imagen.save()

        messages.success(request, "Imágenes subidas correctamente.")
        return redirect('dashboard_anfitrion')

    return render(request, 'WakaTurApp/dashboard_anfitrion.html')



# logout
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')

def tu_funcion_vista(request):
    if request.method == 'POST':
        # Obtener las imágenes del formulario
        imagenes = request.FILES.getlist('imagenes')
        es_principal = request.POST.get('es_principal')
        
        # Aquí debes implementar la lógica para guardar las imágenes
        # Por ejemplo, asociarlas con un alojamiento específico
        
        # Ejemplo (ajustar según tu modelo):
        # alojamiento = Alojamiento.objects.get(propietario=request.user, id=alojamiento_id)
        # for imagen in imagenes:
        #     ImagenAlojamiento.objects.create(
        #         alojamiento=alojamiento,
        #         imagen=imagen,
        #         es_principal=(imagen.name == es_principal)
        #     )
        
        # Redireccionar después de procesar
        return redirect('dashboard_view')
    
    # Si no es POST, redirigir al dashboard
    return redirect('dashboard_view')

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
    return render(request, 'WakaTurApp/registrar_alojamiento.html', {'form': form})