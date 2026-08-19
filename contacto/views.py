from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import ContactForm

def contacto(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            # Construir el mensaje de correo
            contenido = f"""
            El usuario con nombre {nombre} y dirección de email {email} ha enviado el siguiente mensaje:

            Asunto: {asunto}

            Contenido:
            {mensaje}
            """

            email = EmailMessage(
                subject="Mensaje desde App YÚMANO",
                body=contenido,
                from_email="faivertkd@gmail.com",
                to=["faivertkd@gmail.com"],
                reply_to=[email]
            )

            try:
                email.send()
                return redirect("/contacto/?valido")
            except:                 
                 return redirect("/contacto/?novalido")

    return render(request, 'contacto/contacto.html', {'form': form})