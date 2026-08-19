from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, nombre, apellido, tipo_usuario, password=None):
        if not email:
            raise ValueError("El usuario debe tener un email válido")
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario válido")
        
        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            tipo_usuario=tipo_usuario
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, username, email, nombre, apellido, tipo_usuario, password):
        usuario = self.create_user(username, email, nombre, apellido, tipo_usuario, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):  
    TIPOS_USUARIO = [
        ('turista', 'Turista/Viajero'),
        ('cliente_local', 'Cliente Local'),
        ('anfitrion', 'Anfitrión de Alojamientos'),
        ('proveedor_experiencias', 'Proveedor de Experiencias'),
        ('restaurantero', 'Restaurantero/Gastronómico'),
        ('proveedor_servicios', 'Proveedor de Servicios'),
        ('vendedor', 'Vendedor de Tienda'),
        ('admin', 'Administrador'),
        ('soporte', 'Soporte/Atención al Cliente'),
        ('gestor_contenidos', 'Gestor de Contenidos'),
    ]
    username = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, null=True, blank=True, help_text="Número de contacto (WhatsApp)")
    tipo_usuario = models.CharField(max_length=25, choices=TIPOS_USUARIO, default='turista')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verificado = models.BooleanField(default=False, help_text="Prestador verificado por YÚMANO")
    foto_perfil = models.ImageField(upload_to='perfiles', null=True, blank=True, help_text="Foto de perfil")

    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'tipo_usuario']
    
    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"

    def save(self, *args, **kwargs):
        # Si el usuario es de tipo admin, le otorgamos permisos de staff y superuser automáticamente
        if self.tipo_usuario == 'admin':
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    alojamiento = models.ForeignKey('alojamientos.Alojamiento', on_delete=models.CASCADE, null=True, blank=True, related_name='favoritos')
    gastronomia = models.ForeignKey('gastronomia.Gastronomia', on_delete=models.CASCADE, null=True, blank=True, related_name='favoritos')
    experiencia = models.ForeignKey('experiencias.Experiencia', on_delete=models.CASCADE, null=True, blank=True, related_name='favoritos')
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.CASCADE, null=True, blank=True, related_name='favoritos')
    producto = models.ForeignKey('tienda.Producto', on_delete=models.CASCADE, null=True, blank=True, related_name='favoritos')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('usuario', 'alojamiento'),
            ('usuario', 'gastronomia'),
            ('usuario', 'experiencia'),
            ('usuario', 'servicio'),
            ('usuario', 'producto'),
        ]

    def __str__(self):
        return f"Favorito de {self.usuario.username}"
