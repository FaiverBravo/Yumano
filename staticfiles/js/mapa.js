// Creamos un mapa con Leaflet y añadir marcadores personalizados para mostrar información turística de San Agustín, Huila, Colombia
// Autor: Faiver Bravo

class CustomMarker {
    constructor(lat, lng, icon, popupContent) {
        this.lat = lat;
        this.lng = lng;
        this.icon = icon;
        this.popupContent = popupContent;
    }

    createMarker() {
        return L.marker([this.lat, this.lng], {icon: this.icon}).bindPopup(this.popupContent);
    }
}

// Crear iconos personalizados
var geoIcon = new L.Icon({
    iconUrl: staticUrls.geoIcon,
    iconSize: [65, 85],
    iconAnchor: [16, 51],
    popupAnchor: [1, -34]
});

var turismoIcon = new L.Icon({
    iconUrl: staticUrls.turismoIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var alojamientosIcon = new L.Icon({
    iconUrl: staticUrls.alojamientosIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var aventuraIcon = new L.Icon({
    iconUrl: staticUrls.aventuraIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var gastronomiaIcon = new L.Icon({
    iconUrl: staticUrls.gastronomiaIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var contactoIcon = new L.Icon({
    iconUrl: staticUrls.contactoIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var serviciosIcon = new L.Icon({
    iconUrl: staticUrls.serviciosIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var tiendasIcon = new L.Icon({
    iconUrl: staticUrls.tiendasIcon,
    shadowUrl: staticUrls.Shadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// Crear marcadores y grupos de capas
var turismoMarkers = [
    new CustomMarker(1.887648, -76.2949629, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Parque arquelógico San Agustín</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88724803, -76.29549695, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Museo</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88663907, -76.29590293, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Bosque de las Estatuas</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88303662, -76.2943809, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Mesita A</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88419942, -76.29612945, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Mesita B</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88068292, -76.29795741, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Mesita C</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88077357, -76.29916174, turismoIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Fuente Ceremonial de Lavapatas</h4><img width="100%" height="100%" src="' + staticUrls.lavapatasImage + '"><p>informate <a href="https://colombia.travel/es/visita-san-agustin-la-capital-arqueologica-de-colombia" target="_blank">aca</a></p></div>')
];

var turismo = L.layerGroup(turismoMarkers.map(marker => marker.createMarker()));

var alojamientosMarkers = [
    new CustomMarker(1.884916, -76.281095, alojamientosIcon, '<b>Hotel Arqueologico San Agustin</b>'),
    new CustomMarker(1.890318, -76.283683, alojamientosIcon, '<b>Hotel Alto de los Andaquies</b>'),
    new CustomMarker(1.892315, -76.281074, alojamientosIcon, '<b>Akawanka Lodge</b>')
];

var alojamientos = L.layerGroup(alojamientosMarkers.map(marker => marker.createMarker()));

var gastronomiaMarkers = [
    new CustomMarker(1.886418, -76.277312, gastronomiaIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Doña Nury</h4><img width="100%" height="100%" src="' + staticUrls.doñaNury1Image + '"><p>informate <a href="http://127.0.0.1:8000/WakaTurApp/" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.885837, -76.275916, gastronomiaIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Andrés a la Parrilla</h4><img width="100%" height="100%" src="' + staticUrls.r2Image + '"><p>informate <a href="http://127.0.0.1:8000/WakaTurApp/" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.88701, -76.279091, gastronomiaIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Donde Richard</h4><img width="100%" height="100%" src="' + staticUrls.dondeRichard1Image + '"><p>informate <a href="http://127.0.0.1:8000/WakaTurApp/" target="_blank">aca</a></p></div>'),
    new CustomMarker(1.886268, -76.277034, gastronomiaIcon, '<div align="center" style="height: auto; width: 200px;"><h4>Malibú</h4><img width="100%" height="100%" src="' + staticUrls.malibu1Image + '"><p>informate <a href="https://linktr.ee/malibugastrobar" target="_blank">aca</a></p></div>')
];

var gastronomia = L.layerGroup(gastronomiaMarkers.map(marker => marker.createMarker()));

var aventuraMarkers = [
    new CustomMarker(1.885647, -76.275032, aventuraIcon, '<b>Alquiler de Caballos</b>'),
    new CustomMarker(1.882203, -76.277286, aventuraIcon, '<b>Magdalena Rafting</b>'),
    new CustomMarker(1.882963, -76.252714, aventuraIcon, '<b>Adrenalina Extrema Cañon del Magdalena</b>')
];

var aventura = L.layerGroup(aventuraMarkers.map(marker => marker.createMarker()));

var serviciosMarkers = [
    new CustomMarker(1.881476, -76.270762, serviciosIcon, '<b>Cajero ATH Utrahuilca San Agustin I - Banco de Bogotá</b>'),
    new CustomMarker(1.879131, -76.270065, serviciosIcon, '<b>Estacion de gasolina, Sur Andina TERPEL</b>'),
    new CustomMarker(1.881455, -76.271182, serviciosIcon, '<b>Taxis Verdes</b>')
];

var servicios = L.layerGroup(serviciosMarkers.map(marker => marker.createMarker()));

var tiendasMarkers = [
    new CustomMarker(1.884632, -76.273579, tiendasIcon, '<b>Artesanías</b>'),
    new CustomMarker(1.880257, -76.271148, tiendasIcon, '<b>Plaza de Mercado Campesino</b>'),
    new CustomMarker(1.881822, -76.273193, tiendasIcon, '<b>Supermercado Olimpica</b>')
];

var tiendas = L.layerGroup(tiendasMarkers.map(marker => marker.createMarker()));

var contactoMarkers = [
    new CustomMarker(1.886188, -76.277412, contactoIcon, '<div align="center" style="height: auto; width: 200px;font-size: 14px;"><h2>FBRAVO</h2><p>Publica con nosotros</p><img width="100%" height="100%" src="' + staticUrls.logofbravoImage + '"><p>informate <a href="http://127.0.0.1:8000/contacto/"">aca</a></p></div>')
];

var contacto = L.layerGroup(contactoMarkers.map(marker => marker.createMarker()));

// Añadir control de capas
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
});

var esriWorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: 'Tiles © Esri'
});

var osmHOT = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team hosted by OpenStreetMap France'
});

var mapa = L.map('mapa', {
    center: [1.886188, -76.277412],
    zoom: 15,
    layers: [osm, turismo, alojamientos, gastronomia, aventura, servicios, tiendas, contacto]
});

var baseMaps = {
    "OpenStreetMap": osm,
    "Esri World Imagery": esriWorldImagery,
    "OpenStreetMap.HOT": osmHOT    
};

var overlayMaps = {
    "Turismo": turismo,
    "Gastronomía": gastronomia,
    "Alojamientos": alojamientos,
    "Contacto": contacto,
    "Servicios": servicios,
    "Tiendas": tiendas,
    "Aventura": aventura
};

var layerControl = L.control.layers(baseMaps, overlayMaps).addTo(mapa);

// Añadir control de escala con clase personalizada
L.control.scale({
    metric: true,
    imperial: false,
    position: 'topleft',
}).addTo(mapa).getContainer().classList.add('custom-scale-control');

// Función de geolocalización
mapa.locate({setView: true, maxZoom: 16});

function onLocationFound(e) {
    var radius = e.accuracy / 2;

    L.marker(e.latlng, {icon: geoIcon}).bindPopup('<b>Estoy Aquí !</b>').addTo(mapa)
        .bindPopup("Estás a " + radius + " metros de este punto").openPopup();

    L.circle(e.latlng, radius).addTo(mapa);
}

mapa.on('locationfound', onLocationFound);

function onLocationError(e) {
    alert("No es posible encontrar su ubicación. Es posible que tenga que activar la geolocalización.");
}

mapa.on('locationerror', onLocationError);

// Agregar logo
L.Control.Watermark = L.Control.extend({
    onAdd: function(mapa) {
        var img = L.DomUtil.create('img');
        img.src = staticUrls.milestoneIcon;
        img.style.width = '40px';
        return img;
    },
    onRemove: function(mapa) {},
});

L.control.watermark = function(opts) {
    return new L.Control.Watermark({opts});
}
L.control.watermark().addTo(mapa);
