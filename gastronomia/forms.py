from django import forms
from .models import Gastronomia

class GastronomiaForm(forms.ModelForm):
    class Meta:
        model = Gastronomia
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'carta', 'coordenadas', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del plato o servicio'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'carta': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf,image/*'}),
            'coordenadas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitud, Longitud (ej: 1.88, -76.29)'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto (WhatsApp)'}),
        }
