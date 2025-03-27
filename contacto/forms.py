from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Email'})
    )
    asunto = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu Mensaje', 'rows': 4}),
        required=True
    )
