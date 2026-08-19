from django.db import models
from YumanoApp.models import Usuario

# Modelo Categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.nombre

# Modelo Alojamientos
class Alojamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='alojamientos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    coordenadas = models.CharField(max_length=100, help_text="Formato: latitud,longitud (ejemplo: 40.416775,-3.703790)")
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    horario = models.CharField(max_length=100)
    disponibilidad = models.BooleanField(default=True)
    habitaciones_disponibles = models.IntegerField(default=0)
   # imagen_principal = models.ImageField(upload_to='alojamientos/', blank=True, null=True)
   # imagen = models.ImageField(upload_to='alojamientos/')
    telefono = models.CharField(max_length=15, default='', help_text="Número de contacto (WhatsApp)")
    categorias = models.ManyToManyField(Categoria, related_name='alojamientos')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.nombre

# Modelo Imágenes
class ImagenAlojamiento(models.Model):
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='alojamientos/imagenes/')
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    
    class Meta:
        verbose_name = 'imagen'
        verbose_name_plural = 'imágenes'
        ordering = ['orden']
    
    def __str__(self):
        return f"Imagen de {self.alojamiento.nombre}"

    def save(self, *args, **kwargs):
        if self.es_principal:
            # Desmarcar otras imágenes principales del mismo alojamiento
            ImagenAlojamiento.objects.filter(alojamiento=self.alojamiento, es_principal=True).update(es_principal=False)
        super().save(*args, **kwargs)

# Modelo Post para Comentarios/Reseñas
class Post(models.Model):
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.CASCADE, related_name='posts')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    calificacion = models.PositiveIntegerField(default=5, help_text="Calificación de 1 a 5 estrellas")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  

    class Meta:
        verbose_name = 'reseña'
        verbose_name_plural = 'reseñas'
        ordering = ['-created']

    def __str__(self):
        return f"{self.autor.username} - {self.calificacion}★ - {self.descripcion[:50]}"


class Reserva(models.Model):
    alojamiento = models.ForeignKey('Alojamiento', on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    num_personas = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    estado = models.CharField(max_length=20, choices=[
        ('activa', 'Activa'),
        ('Pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada')], default='activa')
    estado_pago = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} en {self.alojamiento.nombre}"
    
    @property
    def dias_estadia(self):
        """Calcula el número de días de estadía."""
        return (self.fecha_fin - self.fecha_inicio).days
