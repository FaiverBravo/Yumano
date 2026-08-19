from django import forms
from .models import Experiencia

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'coordenadas', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la experiencia'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe la actividad', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio por persona'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'coordenadas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitud, Longitud (ej: 1.88, -76.29)'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contacto (WhatsApp)'}),
        }
