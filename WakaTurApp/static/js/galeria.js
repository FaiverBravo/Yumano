// Función para cambiar la imagen principal al hacer clic en una miniatura
function cambiarImagenPrincipal(url) {
    document.getElementById('imagen-principal').src = url;
}

// Función para manejar la selección de imágenes en el formulario
function manejarSeleccionImagenes() {
    const inputImagenes = document.getElementById('imagenes');
    if (!inputImagenes) return; // Si no existe el elemento, no hacer nada
    
    inputImagenes.addEventListener('change', function() {
        const imagenPrincipalSelect = document.getElementById('es_principal');
        if (!imagenPrincipalSelect) return;
        
        imagenPrincipalSelect.innerHTML = '<option value="">Seleccionar imagen principal</option>';
        
        for (let i = 0; i < this.files.length; i++) {
            const option = document.createElement('option');
            option.value = this.files[i].name;
            option.textContent = this.files[i].name;
            imagenPrincipalSelect.appendChild(option);
        }
    });
}

// Inicializar las funciones cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    manejarSeleccionImagenes();
});