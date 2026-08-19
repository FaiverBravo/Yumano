// Creamos un mapa con Leaflet y añadir marcadores personalizados para mostrar información turística de San Agustín, Huila, Colombia
// Autor: Faiver Bravo

var userLocation = null;
var routingControl = null;

class CustomMarker {
    constructor(lat, lng, icon, title, content = '') {
        this.lat = lat;
        this.lng = lng;
        this.icon = icon;
        this.title = title;
        this.content = content;
    }

    createMarker() {
        const popupContent = `
            <div class="map-popup-modern" style="width: 220px;">
                <h5 class="fw-bold mb-2">${this.title}</h5>
                ${this.content}
                <div class="d-grid gap-2 mt-3">
                    <button class="btn btn-premium btn-sm rounded-pill" onclick="startRouting(${this.lat}, ${this.lng}, '${this.title}')">
                        <i class="fas fa-directions me-1"></i> Ir ahora
                    </button>
                    <a href="https://www.google.com/maps/dir/?api=1&destination=${this.lat},${this.lng}" target="_blank" class="btn btn-outline-dark btn-sm rounded-pill">
                        <i class="fab fa-google me-1"></i> Google Maps
                    </a>
                </div>
            </div>
        `;
        return L.marker([this.lat, this.lng], {icon: this.icon}).bindPopup(popupContent);
    }
}

// Crear iconos personalizados
var geoIcon = new L.Icon({
    iconUrl: staticUrls.geoIcon,
    iconSize: [65, 85],
    iconAnchor: [16, 51],
    popupAnchor: [1, -34]
});

var createStandardIcon = (url) => new L.Icon({
    iconUrl: url,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var turismoIcon = createStandardIcon(staticUrls.turismoIcon);
var alojamientosIcon = createStandardIcon(staticUrls.alojamientosIcon);
var aventuraIcon = createStandardIcon(staticUrls.aventuraIcon);
var gastronomiaIcon = createStandardIcon(staticUrls.gastronomiaIcon);
var contactoIcon = createStandardIcon(staticUrls.contactoIcon);
var serviciosIcon = createStandardIcon(staticUrls.serviciosIcon);
var tiendasIcon = createStandardIcon(staticUrls.tiendasIcon);

// Grupos de capas
var turismo = L.layerGroup();
var alojamientos = L.layerGroup();
var gastronomia = L.layerGroup();
var aventura = L.layerGroup();
var servicios = L.layerGroup();
var tiendas = L.layerGroup();
var contacto = L.layerGroup();

// Cargar datos dinámicos
fetch('/api/map-data/')
    .then(response => response.json())
    .then(data => {
        // Alojamientos
        data.alojamientos.forEach(item => {
            const content = item.imagen ? `<img width="100%" class="rounded-3 mb-2" src="${item.imagen}"><p class="small mb-0">${item.descripcion}</p>` : `<p class="small mb-0">${item.descripcion}</p>`;
            new CustomMarker(item.lat, item.lng, alojamientosIcon, item.nombre, content)
                .createMarker().addTo(alojamientos);
        });

        // Gastronomía
        data.gastronomia.forEach(item => {
            const content = item.imagen ? `<img width="100%" class="rounded-3 mb-2" src="${item.imagen}"><p class="small mb-0">${item.descripcion}</p>` : `<p class="small mb-0">${item.descripcion}</p>`;
            new CustomMarker(item.lat, item.lng, gastronomiaIcon, item.nombre, content)
                .createMarker().addTo(gastronomia);
        });

        // Experiencias (Aventura)
        data.experiencias.forEach(item => {
            const content = item.imagen ? `<img width="100%" class="rounded-3 mb-2" src="${item.imagen}"><p class="small mb-0">${item.descripcion}</p>` : `<p class="small mb-0">${item.descripcion}</p>`;
            new CustomMarker(item.lat, item.lng, aventuraIcon, item.nombre, content)
                .createMarker().addTo(aventura);
        });

        // Servicios
        data.servicios.forEach(item => {
            const content = item.imagen ? `<img width="100%" class="rounded-3 mb-2" src="${item.imagen}"><p class="small mb-0">${item.descripcion}</p>` : `<p class="small mb-0">${item.descripcion}</p>`;
            new CustomMarker(item.lat, item.lng, serviciosIcon, item.nombre, content)
                .createMarker().addTo(servicios);
        });
    });

// Marcadores Estáticos (Turismo y Contacto)
var turismoMarkers = [
    new CustomMarker(1.887648, -76.2949629, turismoIcon, 'Parque Arqueológico', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}"><p class="small mb-0">Capital arqueológica de Colombia.</p>`),
    new CustomMarker(1.88724803, -76.29549695, turismoIcon, 'Museo Arqueológico', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.88663907, -76.29590293, turismoIcon, 'Bosque de las Estatuas', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.88303662, -76.2943809, turismoIcon, 'Mesita A', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.88419942, -76.29612945, turismoIcon, 'Bosque de las Estatuas B', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.88068292, -76.29795741, turismoIcon, 'Bosque de las Estatuas C', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.88077357, -76.29916174, turismoIcon, 'Fuente de Lavapatas', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.880354,-76.303214, turismoIcon, 'Fuente de Lavapatas', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`),
    new CustomMarker(1.890394, -76.381300, turismoIcon, 'Cascada Los Tres Chorros', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.lavapatasImage}">`), 
    
];
turismoMarkers.forEach(m => m.createMarker().addTo(turismo));

var contactoMarkers = [
    new CustomMarker(1.886188, -76.277412, contactoIcon, 'FBRAVO Support', `<img width="100%" class="rounded-3 mb-2" src="${staticUrls.logofbravoImage}"><p class="small">Publica con nosotros.</p>`)
];
contactoMarkers.forEach(m => m.createMarker().addTo(contacto));

// Añadir control de capas
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap' });
var esriWorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Tiles © Esri' });
var osmHOT = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap France' });

var mapa = L.map('mapa', {
    center: [1.886188, -76.277412],
    zoom: 15,
    zoomControl: false,
    layers: [osm, turismo, alojamientos, gastronomia, aventura, servicios, tiendas, contacto]
});

// Re-añadir control de zoom en una posición más cómoda
L.control.zoom({ position: 'bottomright' }).addTo(mapa);

// El control nativo L.control.layers ha sido eliminado para usar los chips de filtro y el conmutador premium satelital.

// Control de Escala
L.control.scale({ metric: true, imperial: false, position: 'bottomleft' }).addTo(mapa);

// Lógica de Ruteo
function startRouting(destLat, destLng, destName) {
    if (!userLocation) {
        alert("Primero necesitamos conocer tu ubicación. Por favor, activa el GPS.");
        mapa.locate({setView: true, maxZoom: 16});
        return;
    }

    if (routingControl) {
        mapa.removeControl(routingControl);
    }

    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(userLocation.lat, userLocation.lng),
            L.latLng(destLat, destLng)
        ],
        language: 'es',
        routeWhileDragging: true,
        showAlternatives: true,
        createMarker: function() { return null; }, // No crear marcadores extra
        lineOptions: {
            styles: [{ color: '#2D5A27', opacity: 0.8, weight: 6 }]
        }
    }).addTo(mapa);

    // Mostrar panel de instrucciones
    document.getElementById('routing-panel').classList.remove('d-none');
    routingControl.on('routesfound', function(e) {
        const routes = e.routes;
        const summary = routes[0].summary;
        const detailsHtml = `
            <div class="p-2">
                <p class="mb-1 text-success"><b>Destino:</b> ${destName}</p>
                <div class="d-flex justify-content-between mb-2">
                    <span><i class="fas fa-car me-1"></i> ${(summary.totalDistance / 1000).toFixed(1)} km</span>
                    <span><i class="fas fa-clock me-1"></i> ${Math.round(summary.totalTime / 60)} min</span>
                </div>
                <hr class="my-2">
                <div class="instructions-list small">
                    ${routes[0].instructions.map(i => `<div class="mb-1 border-bottom pb-1">${i.text}</div>`).join('')}
                </div>
            </div>
        `;
        document.getElementById('routing-details').innerHTML = detailsHtml;
    });
    
    mapa.closePopup();
}

function closeRouting() {
    if (routingControl) {
        mapa.removeControl(routingControl);
        routingControl = null;
    }
    document.getElementById('routing-panel').classList.add('d-none');
}

// Geolocalización mejorada
mapa.locate({setView: true, maxZoom: 16});

mapa.on('locationfound', function(e) {
    userLocation = e.latlng;
    var radius = e.accuracy / 2;

    if (window.userMarker) {
        mapa.removeLayer(window.userMarker);
        mapa.removeLayer(window.userCircle);
    }

    window.userMarker = L.marker(e.latlng, {icon: geoIcon}).addTo(mapa).bindPopup("Estás aquí (margen de " + Math.round(radius) + "m)");
    window.userCircle = L.circle(e.latlng, radius, { color: '#2D5A27', fillColor: '#2D5A27', fillOpacity: 0.1 }).addTo(mapa);
});

mapa.on('locationerror', function() {
    console.log("Error de geolocalización");
});

// El botón nativo de geolocalización ha sido removido porque ya contamos con el botón flotante premium en el HTML.

// Marca de agua
L.control.watermark = function() {
    return new (L.Control.extend({
        onAdd: function() {
            var img = L.DomUtil.create('img');
            img.src = staticUrls.milestoneIcon;
            img.style.width = '40px';
            img.style.opacity = '0.7';
            return img;
        }
    }))();
};
L.control.watermark({ position: 'bottomleft' }).addTo(mapa);

// ===== FILTROS Y BÚSQUEDA =====
var layerMap = {
    turismo: turismo,
    alojamientos: alojamientos,
    gastronomia: gastronomia,
    aventura: aventura,
    servicios: servicios,
    tiendas: tiendas,
    contacto: contacto
};

function toggleAllLayers(btn) {
    // Activar todas las capas
    document.querySelectorAll('.chip-filter').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    Object.values(layerMap).forEach(layer => {
        if (!mapa.hasLayer(layer)) mapa.addLayer(layer);
    });
}

function toggleSingleLayer(btn, layerName) {
    // Desactivar "Todos"
    document.querySelector('.chip-filter[data-layer="all"]').classList.remove('active');

    btn.classList.toggle('active');

    var layer = layerMap[layerName];
    if (!layer) return;

    if (btn.classList.contains('active')) {
        if (!mapa.hasLayer(layer)) mapa.addLayer(layer);
    } else {
        if (mapa.hasLayer(layer)) mapa.removeLayer(layer);
    }

    // Si ninguno activo, reactivar todos
    var anyActive = document.querySelectorAll('.chip-filter.active:not([data-layer="all"])');
    if (anyActive.length === 0) {
        document.querySelector('.chip-filter[data-layer="all"]').classList.add('active');
        Object.values(layerMap).forEach(l => { if (!mapa.hasLayer(l)) mapa.addLayer(l); });
    }
}

// Búsqueda de marcadores
document.getElementById('map-search-input').addEventListener('input', function(e) {
    var query = e.target.value.toLowerCase().trim();
    if (query.length < 2) return;

    // Buscar en todos los layers
    var found = false;
    Object.values(layerMap).forEach(function(group) {
        group.eachLayer(function(marker) {
            if (marker.getPopup) {
                var popup = marker.getPopup();
                if (popup) {
                    var content = popup.getContent().toLowerCase();
                    if (content.includes(query) && !found) {
                        mapa.flyTo(marker.getLatLng(), 17);
                        marker.openPopup();
                        found = true;
                    }
                }
            }
        });
    });
});

// Mi Ubicación botón flotante
document.getElementById('locate-btn').addEventListener('click', function() {
    if ("geolocation" in navigator) {
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        var self = this;
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            userLocation = L.latLng(lat, lng);
            
            if (window.userMarker) {
                window.userMarker.setLatLng([lat, lng]);
            } else {
                window.userMarker = L.marker([lat, lng], {icon: geoIcon}).addTo(mapa)
                    .bindPopup("<div class='text-center fw-bold'>Estás aquí</div>");
            }
            mapa.flyTo([lat, lng], 16);
            self.innerHTML = '<i class="fas fa-crosshairs"></i>';
        }, function(error) {
            alert("No se pudo obtener tu ubicación. Activa el GPS.");
            self.innerHTML = '<i class="fas fa-crosshairs"></i>';
        }, { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 });
    } else {
        alert("Tu navegador no soporta geolocalización.");
    }
});

// ===== CONTROL DE CAPA BASE (ESTÁNDAR / SATÉLITE) =====
document.getElementById('btn-map-standard').addEventListener('click', function() {
    if (!mapa.hasLayer(osm)) {
        mapa.addLayer(osm);
    }
    if (mapa.hasLayer(esriWorldImagery)) {
        mapa.removeLayer(esriWorldImagery);
    }
    this.classList.add('active');
    document.getElementById('btn-map-satellite').classList.remove('active');
});

document.getElementById('btn-map-satellite').addEventListener('click', function() {
    if (!mapa.hasLayer(esriWorldImagery)) {
        mapa.addLayer(esriWorldImagery);
    }
    if (mapa.hasLayer(osm)) {
        mapa.removeLayer(osm);
    }
    this.classList.add('active');
    document.getElementById('btn-map-standard').classList.remove('active');
});
