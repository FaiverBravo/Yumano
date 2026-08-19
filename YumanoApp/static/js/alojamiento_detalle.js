/**
 * YÚMANO - Alojamiento Detalle Interactivity
 * Galería de fotos, mapa Leaflet sin secuestro de scroll y calculadora de precios
 */

// 1. Galería de Imágenes y Contador
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('galeriaCarousel');
    if (carousel) {
        const counter = document.getElementById('carouselCounter');
        const thumbs = document.querySelectorAll('.gallery-thumb');
        const totalSlides = thumbs.length;

        // Sincronizar miniaturas y contador al deslizar
        carousel.addEventListener('slid.bs.carousel', function(e) {
            const index = e.to;
            thumbs.forEach(t => t.classList.remove('active'));
            if (thumbs[index]) thumbs[index].classList.add('active');
            if (counter) counter.textContent = (index + 1) + ' / ' + totalSlides;
        });
    }
});

// 2. Inicialización del Mapa de Ubicación (Leaflet)
document.addEventListener('DOMContentLoaded', function() {
    const mapElem = document.getElementById('map');
    if (!mapElem || typeof L === 'undefined') return;

    // Coordenadas por defecto (San Agustín, Huila)
    let lat = 1.886188, lng = -76.277412;
    const coordStr = mapElem.dataset.coordenadas || '';

    if (coordStr && coordStr.includes(',')) {
        const parts = coordStr.split(',');
        const parsedLat = parseFloat(parts[0].trim());
        const parsedLng = parseFloat(parts[1].trim());
        if (!isNaN(parsedLat) && !isNaN(parsedLng)) {
            lat = parsedLat;
            lng = parsedLng;
        }
    }

    const nombre = mapElem.dataset.nombre || 'Alojamiento';
    const direccion = mapElem.dataset.direccion || 'San Agustín, Huila';

    // Crear mapa con scrollWheelZoom deshabilitado por defecto para facilitar el desplazamiento de la página
    const map = L.map('map', {
        scrollWheelZoom: false,
        touchZoom: true,
        dragging: true
    }).setView([lat, lng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | YÚMANO'
    }).addTo(map);

    const popupContent = `
        <div style="font-family: inherit; font-size: 13px; line-height: 1.4; padding: 4px;">
            <strong style="color: #2D5A27; font-size: 14px; display: block; margin-bottom: 2px;">${nombre}</strong>
            <span style="color: #6c757d; font-size: 12px;"><i class="fas fa-map-marker-alt text-danger me-1"></i>${direccion}</span>
            <div style="margin-top: 8px; border-top: 1px solid #eee; padding-top: 6px;">
                <a href="https://www.google.com/maps/search/?api=1&query=${lat},${lng}" target="_blank" rel="noopener noreferrer" style="color: #FA9E1B; font-weight: 600; text-decoration: none; font-size: 12px;">
                    📍 Abrir en Google Maps &rarr;
                </a>
            </div>
        </div>
    `;

    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(popupContent).openPopup();

    // Habilitar zoom con rueda solo si el usuario hace clic dentro del mapa
    map.on('focus', function() { map.scrollWheelZoom.enable(); });
    map.on('blur', function() { map.scrollWheelZoom.disable(); });
});

// 3. Calculadora Dinámica de Precios de Reserva
document.addEventListener('DOMContentLoaded', function() {
    const mapElem = document.getElementById('map');
    const startInput = document.getElementById('fecha_inicio');
    const endInput = document.getElementById('fecha_fin');
    const summary = document.getElementById('priceSummary');
    
    if (!startInput || !endInput || !summary) return;

    // Obtener precio por noche del dataset del mapa o del formulario
    const pricePerNight = mapElem ? parseFloat(mapElem.dataset.precio || '0') : 0;

    function calculate() {
        if (startInput.value && endInput.value) {
            const start = new Date(startInput.value);
            const end = new Date(endInput.value);
            
            if (end > start) {
                const diffTime = Math.abs(end - start);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                if (diffDays > 0) {
                    const total = diffDays * pricePerNight;
                    const daysCountElem = document.getElementById('daysCount');
                    const basePriceElem = document.getElementById('basePrice');
                    const totalPriceElem = document.getElementById('totalPrice');

                    if (daysCountElem) daysCountElem.innerText = diffDays;
                    if (basePriceElem) basePriceElem.innerText = `$ ${total.toLocaleString('es-CO')} COP`;
                    if (totalPriceElem) totalPriceElem.innerText = `$ ${total.toLocaleString('es-CO')} COP`;
                    
                    summary.classList.remove('d-none');
                }
            } else {
                summary.classList.add('d-none');
            }
        }
    }

    startInput.addEventListener('change', calculate);
    endInput.addEventListener('change', calculate);
});
