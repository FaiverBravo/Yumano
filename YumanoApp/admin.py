from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'nombre', 'apellido', 'tipo_usuario', 'is_staff', 'is_superuser', 'is_active')  #  Campos visibles en la tabla
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')  #  Filtros laterales
    search_fields = ('username', 'email', 'nombre', 'apellido')  #  Barra de búsqueda
    ordering = ('username',)  # Orden por defecto
    filter_horizontal = ()
    
    fieldsets = (
        ('Información Personal', {'fields': ('username', 'email', 'nombre', 'apellido', 'tipo_usuario')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Fechas', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        ('Crear Nuevo Usuario', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombre', 'apellido', 'tipo_usuario', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(Usuario, UsuarioAdmin)

# Cambiar el título del panel de administración
admin.site.site_header = "Panel de Administración YÚMANO"
admin.site.site_title = "Admin YÚMANO"
admin.site.index_title = "Gestión de Usuarios y Servicios"

