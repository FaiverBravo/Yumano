/**
 * YÚMANO - Global Theme & UI Controllers
 * Manejo de Modo Oscuro, Toasts, Favoritos Globales, Búsqueda y Navegación Móvil
 */

// --- TOAST SYSTEM ---
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    let iconClass = 'fa-info-circle text-info';
    let title = 'Información';
    if (type === 'success') {
        iconClass = 'fa-check-circle text-success';
        title = 'Éxito';
    } else if (type === 'warning') {
        iconClass = 'fa-exclamation-triangle text-warning';
        title = 'Advertencia';
    } else if (type === 'danger') {
        iconClass = 'fa-times-circle text-danger';
        title = 'Error';
    }

    const toastId = 'toast-' + Math.random().toString(36).substr(2, 9);
    const toastHTML = `
        <div id="${toastId}" class="custom-toast toast-type-${type} shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="custom-toast-body d-flex align-items-center">
                <div class="toast-icon me-3">
                    <i class="fas ${iconClass} fa-lg"></i>
                </div>
                <div class="toast-content flex-grow-1">
                    <strong class="toast-title d-block">${title}</strong>
                    <span class="toast-msg small text-secondary">${message}</span>
                </div>
                <button type="button" class="btn-close ms-2 custom-toast-close" aria-label="Close" onclick="closeToast('${toastId}')"></button>
            </div>
            <div class="toast-progress">
                <div class="toast-progress-bar bg-${type === 'danger' ? 'danger' : type}"></div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHTML);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        closeToast(toastId);
    }, 5000);
}

function closeToast(id) {
    const toast = document.getElementById(id);
    if (toast) {
        toast.classList.add('hide-toast');
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }
}

// --- THEME & UI CONTROLLER INICIALIZACIÓN ---
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const themeToggleMobile = document.getElementById('themeToggleMobile');
    const themeIconMobile = document.querySelector('.themeIconMobile');
    const root = document.documentElement;

    // Función para actualizar icono según tema actual
    const updateIcon = () => {
        const isDark = root.getAttribute('data-bs-theme') === 'dark';
        if (isDark) {
            if (themeIcon) { themeIcon.className = 'fas fa-sun'; }
            if (themeIconMobile) { themeIconMobile.className = 'fas fa-sun themeIconMobile'; }
        } else {
            if (themeIcon) { themeIcon.className = 'fas fa-moon'; }
            if (themeIconMobile) { themeIconMobile.className = 'fas fa-moon themeIconMobile'; }
        }
    };

    // Icono inicial
    updateIcon();

    const toggleTheme = () => {
        const currentTheme = root.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        if (newTheme === 'dark') {
            root.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            root.removeAttribute('data-bs-theme');
            localStorage.setItem('theme', 'light');
        }
        updateIcon();
    };

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    if (themeToggleMobile) themeToggleMobile.addEventListener('click', toggleTheme);

    // Active Class Logic for Mobile Navigation
    const currentPath = window.location.pathname;
    const currentHash = window.location.hash;

    const navInicio = document.getElementById('mobile-nav-inicio');
    const navMapa = document.getElementById('mobile-nav-mapa');
    const navFavoritos = document.getElementById('mobile-nav-favoritos');
    const navPanel = document.getElementById('mobile-nav-panel');
    const navEntrar = document.getElementById('mobile-nav-entrar');

    if (currentPath === '/' || currentPath === '/index.html' || currentPath === '/Inicio/') {
        if (navInicio) navInicio.classList.add('active');
    } else if (currentPath.includes('/mapa') || currentPath.includes('/Mapa')) {
        if (navMapa) navMapa.classList.add('active');
    } else if (currentPath.includes('/login') || currentPath.includes('/registro')) {
        if (navEntrar) navEntrar.classList.add('active');
        if (navPanel) navPanel.classList.add('active');
    } else if (currentPath.includes('/dashboard')) {
        if (currentHash === '#favoritos-section') {
            if (navFavoritos) navFavoritos.classList.add('active');
        } else {
            if (navPanel) navPanel.classList.add('active');
        }
    }

    // Sync favorites nav item if hash changes dynamically
    window.addEventListener('hashchange', () => {
        if (window.location.hash === '#favoritos-section') {
            if (navPanel) navPanel.classList.remove('active');
            if (navFavoritos) navFavoritos.classList.add('active');
        } else {
            if (navFavoritos) navFavoritos.classList.remove('active');
            if (navPanel) navPanel.classList.add('active');
        }
    });

    // --- GLOBAL SEARCH MODAL CONTROLLER ---
    const searchModal = document.getElementById('searchModal');
    const openSearchBtns = document.querySelectorAll('.open-search-btn');
    const closeSearchBtn = document.getElementById('closeSearchBtn');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchChips = document.querySelectorAll('.search-chip');

    let currentType = 'all';
    let debounceTimer;

    openSearchBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            if (searchModal) {
                searchModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
                setTimeout(() => searchInput.focus(), 150);
            }
        });
    });

    function closeModal() {
        if (searchModal) {
            searchModal.style.display = 'none';
            document.body.style.overflow = '';
            if (searchInput) searchInput.value = '';
            resetResults();
        }
    }

    if (closeSearchBtn) {
        closeSearchBtn.addEventListener('click', closeModal);
    }

    if (searchModal) {
        searchModal.addEventListener('click', function (e) {
            if (e.target === searchModal) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && searchModal && searchModal.style.display === 'flex') {
            closeModal();
        }
    });

    searchChips.forEach(chip => {
        chip.addEventListener('click', function () {
            searchChips.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            currentType = this.getAttribute('data-type');
            performSearch();
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(performSearch, 300);
        });
    }

    function resetResults() {
        if (searchResults) {
            searchResults.innerHTML = `
                <div class="search-initial-state">
                    <i class="fas fa-search mb-3 text-muted" style="font-size: 2.5rem;"></i>
                    <p class="text-secondary">Escribe algo para buscar alojamientos, restaurantes, experiencias, artesanías y más...</p>
                </div>
            `;
        }
    }

    function performSearch() {
        if (!searchInput) return;
        const query = searchInput.value.trim();
        if (query.length < 2) {
            if (query.length === 0) {
                resetResults();
            }
            return;
        }

        if (searchResults) {
            searchResults.innerHTML = `
                <div class="search-loading-state">
                    <div class="spinner-border text-success" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="text-secondary mt-3">Buscando en YÚMANO...</p>
                </div>
            `;
        }

        fetch(`/api/search/?q=${encodeURIComponent(query)}&type=${currentType}`)
            .then(response => response.json())
            .then(data => {
                renderResults(data);
            })
            .catch(err => {
                console.error('Error in search:', err);
                if (searchResults) {
                    searchResults.innerHTML = `
                        <div class="search-empty-state">
                            <i class="fas fa-exclamation-circle mb-3 text-danger" style="font-size: 2.5rem;"></i>
                            <p class="text-secondary">Ocurrió un error al realizar la búsqueda. Inténtalo de nuevo.</p>
                        </div>
                    `;
                }
            });
    }

    function renderResults(data) {
        if (!searchResults) return;
        searchResults.innerHTML = '';

        let hasResults = false;
        const groups = {
            alojamientos: { title: 'Alojamientos', items: data.alojamientos || [], icon: 'fa-bed' },
            experiencias: { title: 'Experiencias', items: data.experiencias || [], icon: 'fa-hiking' },
            gastronomia: { title: 'Gastronomía', items: data.gastronomia || [], icon: 'fa-utensils' },
            tienda: { title: 'Artesanías', items: data.tienda || [], icon: 'fa-store' },
            servicios: { title: 'Servicios', items: data.servicios || [], icon: 'fa-concierge-bell' }
        };

        for (const key in groups) {
            const group = groups[key];
            if (group.items.length > 0) {
                hasResults = true;
                let groupHTML = `
                    <div class="search-result-group">
                        <div class="search-result-group-title">
                            <i class="fas ${group.icon} me-2"></i>${group.title}
                        </div>
                `;

                group.items.forEach(item => {
                    const imgHTML = item.imagen
                        ? `<img src="${item.imagen}" class="search-result-thumb" alt="${item.nombre}">`
                        : `<div class="search-result-thumb d-flex align-items-center justify-content-center bg-success text-white"><i class="fas ${group.icon}"></i></div>`;

                    const priceHTML = item.precio
                        ? `<span class="search-result-price">$${parseInt(item.precio).toLocaleString('es-CO')}</span>`
                        : '';

                    groupHTML += `
                        <a href="${item.url}" class="search-result-item">
                            ${imgHTML}
                            <div class="search-result-info">
                                <div class="search-result-name">${item.nombre}</div>
                                <div class="search-result-desc">${item.descripcion || ''}</div>
                            </div>
                            ${priceHTML}
                        </a>
                    `;
                });

                groupHTML += `</div>`;
                searchResults.insertAdjacentHTML('beforeend', groupHTML);
            }
        }

        if (!hasResults) {
            searchResults.innerHTML = `
                <div class="search-empty-state">
                    <i class="fas fa-search-minus mb-3 text-muted" style="font-size: 2.5rem;"></i>
                    <p class="text-secondary mb-0">No se encontraron resultados para tu búsqueda.</p>
                    <small class="text-muted">Prueba con otras palabras o cambia de categoría.</small>
                </div>
            `;
        }
    }

    // --- SCROLL REVEAL OBSERVER ---
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if (revealElements.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px 0px -80px 0px',
            threshold: 0.1
        };

        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        revealElements.forEach(el => {
            revealObserver.observe(el);
        });
    }
});

// --- GLOBAL FAVORITES HANDLER WITH TOAST FEEDBACK ---
document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-tipo][data-id]');
    if (btn && (btn.classList.contains('fav-btn') || btn.innerText.includes('favoritos'))) {
        e.preventDefault();
        const tipo = btn.getAttribute('data-tipo');
        const id = btn.getAttribute('data-id');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

        const formData = new FormData();
        formData.append('tipo', tipo);
        formData.append('id', id);

        fetch('/toggle-favorito/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
            .then(response => {
                if (response.status === 401 || response.status === 403) {
                    showToast('Debes iniciar sesión para guardar favoritos.', 'warning');
                    setTimeout(() => {
                        window.location.href = '/login/';
                    }, 1200);
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && data.status === 'success') {
                    if (data.active) {
                        btn.className = btn.className.replace('btn-outline-secondary', 'btn-outline-danger');
                        if (!btn.className.includes('btn-outline-danger')) {
                            btn.classList.add('btn-outline-danger');
                        }
                        if (btn.innerHTML.includes('favorito') || btn.innerText.includes('favorito')) {
                            btn.innerHTML = `<i class="fas fa-heart me-2 text-danger"></i>En favoritos`;
                        }

                        // Heartbeat micro-animation
                        btn.classList.add('heartbeat-animation');
                        btn.addEventListener('animationend', () => {
                            btn.classList.remove('heartbeat-animation');
                        }, { once: true });

                        showToast("Añadido a tus favoritos", "success");
                    } else {
                        btn.className = btn.className.replace('btn-outline-danger', 'btn-outline-secondary');
                        if (!btn.className.includes('btn-outline-secondary')) {
                            btn.classList.add('btn-outline-secondary');
                        }
                        if (btn.innerHTML.includes('favorito') || btn.innerText.includes('favorito')) {
                            btn.innerHTML = `<i class="far fa-heart me-2"></i>Guardar en favoritos`;
                        }

                        showToast("Eliminado de tus favoritos", "info");

                        const card = btn.closest('.fav-item-card');
                        if (card) {
                            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                            card.style.opacity = '0';
                            card.style.transform = 'scale(0.9)';
                            setTimeout(() => card.remove(), 400);
                        }
                    }
                }
            })
            .catch(err => {
                console.error('Error toggling favorite:', err);
                showToast('Ocurrió un error al procesar tu solicitud.', 'danger');
            });
    }
});
