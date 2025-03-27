# alojamientos/forms.py
from django import forms
from .models import Alojamiento, ImagenAlojamiento

class ImagenAlojamientoForm(forms.ModelForm):
    class Meta:
        model = ImagenAlojamiento
        fields = ['imagen', 'es_principal', 'orden']

class AlojamientoForm(forms.ModelForm):
    class Meta:
        model = Alojamiento
        fields = ['nombre', 'direccion', 'coordenadas']