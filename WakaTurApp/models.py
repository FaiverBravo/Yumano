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
    tipo_usuario = models.CharField(max_length=25, choices=TIPOS_USUARIO, default='turista')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  

    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'tipo_usuario']
    
    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"
