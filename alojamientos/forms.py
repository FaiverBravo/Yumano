# alojamientos/forms.py
from django import forms
from .models import Alojamiento

class AlojamientoForm(forms.ModelForm):
    class Meta:
        model = Alojamiento
        fields = ['nombre', 'direccion', 'coordenadas', 'telefono']