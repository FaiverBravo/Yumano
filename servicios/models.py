from django.db import models
from YumanoApp.models import Usuario

# Create your models here.

class Servicio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicios', null=True, blank=True)
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=50)
    precio=models.IntegerField()
    imagen=models.ImageField(upload_to='servicios')
    coordenadas = models.CharField(max_length=100, null=True, blank=True, help_text="Formato: latitud,longitud")
    disponibilidad = models.BooleanField(default=True)
    horario = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, default='', help_text="Número de contacto (WhatsApp)")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='servicio'
        verbose_name_plural='servicios'

    def __str__(self):
        return self.nombre