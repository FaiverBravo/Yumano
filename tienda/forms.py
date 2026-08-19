from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categorias', 'precio', 'imagen', 'descripcion', 'telefono', 'disponibilidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto o artesanía'}),
            'categorias': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en COP'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe tu producto o artesanía...', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto (WhatsApp)'}),
            'disponibilidad': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
