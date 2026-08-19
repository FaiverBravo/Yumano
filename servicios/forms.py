from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'coordenadas', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'coordenadas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitud, Longitud (ej: 1.88, -76.29)'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto (WhatsApp)'}),
        }
