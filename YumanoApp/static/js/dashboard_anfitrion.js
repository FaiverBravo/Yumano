document.addEventListener('DOMContentLoaded', function() {
    // Manejo del toggle de disponibilidad rápida
    const toggles = document.querySelectorAll('.availability-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const id = this.getAttribute('data-id');
            const tipo = this.getAttribute('data-tipo');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
            const isChecked = this.checked;
            
            const formData = new FormData();
            formData.append('id', id);
            formData.append('tipo', tipo);
            
            fetch('/toggle-disponibilidad/', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if(data.status === 'success') {
                    this.checked = data.active;
                    showToast('Disponibilidad actualizada exitosamente', 'success');
                } else {
                    showToast(data.message || 'Error al actualizar disponibilidad', 'danger');
                    this.checked = !isChecked;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isChecked;
                showToast('Ocurrió un error de red al actualizar disponibilidad.', 'danger');
            });
        });
    });
});
