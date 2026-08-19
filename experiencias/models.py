from django.db import models
from YumanoApp.models import Usuario

# Create your models here.

class Experiencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='experiencias', null=True, blank=True)
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=250)
    precio=models.IntegerField()
    imagen=models.ImageField(upload_to='experiencias')
    coordenadas = models.CharField(max_length=100, null=True, blank=True, help_text="Formato: latitud,longitud")
    disponibilidad = models.BooleanField(default=True)
    horario = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, default='', help_text="Número de contacto (WhatsApp)")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='experiencia'
        verbose_name_plural='experiencias'

    def __str__(self):
        return self.nombre