// 1. BASE DE DATOS LOCAL DINÁMICA DE ADMINISTRADORES
    let admins = [
        { id: 1, name: 'Ricardo Valdivia', email: 'r.valdivia@yumano.com', sector: 'Hoteles', role: 'Gestor Senior', status: 'Conectado' },
        { id: 2, name: 'Ana Castillo', email: 'a.castillo@yumano.com', sector: 'Gastronomía', role: 'Supervisora', status: 'Ausente' },
        { id: 3, name: 'Julian Soler', email: 'j.soler@yumano.com', sector: 'Tiendas', role: 'Logística', status: 'Conectado' }
    ];

    // Colores de fondos/letras según sector (DESIGN.md)
    const sectorStyles = {
        'Hoteles': 'background: #D0E9D4; color: #0B2013;', // primary-fixed
        'Gastronomía': 'background: #FFDAD2; color: #802915;', // secondary-fixed
        'Tiendas': 'background: #FFDCC4; color: #613F24;', // tertiary-fixed
        'Experiencias': 'background: #d0e9d4; color: #364c3c;',
        'Servicios': 'background: #e5e2dd; color: #434843;'
    };

    // Renderizar tabla
    function renderAdminsTable() {
        const tbody = document.getElementById('admins-table-body');
        tbody.innerHTML = '';

        admins.forEach(admin => {
            const initials = admin.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            
            // Elegir un color de avatar aleatorio/estético basado en su nombre
            let bgAvatar = '#fe876b';
            if(admin.id % 3 === 1) bgAvatar = '#d0e9d4';
            if(admin.id % 3 === 2) bgAvatar = '#ffdcc4';
            
            let colorAvatar = '#061b0e';
            if(admin.id % 3 === 1) colorAvatar = '#0b2013';
            if(admin.id % 3 === 2) colorAvatar = '#613f24';

            const styleBadge = sectorStyles[admin.sector] || 'background: #e5e2dd; color: #1c1c19;';
            const statusClass = admin.status === 'Conectado' ? 'status-connected' : 'status-absent';

            const tr = document.createElement('tr');
            tr.id = `admin-row-${admin.id}`;
            tr.innerHTML = `
                <td>
                    <div class="admin-name-cell">
                        <div class="admin-avatar-letters" style="background: ${bgAvatar}; color: ${colorAvatar};">
                            ${initials}
                        </div>
                        <div>
                            <strong style="color: #061b0e;">${admin.name}</strong>
                            <span class="admin-email-text">${admin.email}</span>
                        </div>
                    </div>
                </td>
                <td>
                    <span class="badge-sector-heritage" style="${styleBadge}">${admin.sector}</span>
                </td>
                <td style="color: #434843; font-weight: 500;">${admin.role}</td>
                <td>
                    <span class="status-dot-heritage ${statusClass}">${admin.status}</span>
                </td>
                <td>
                    <button class="btn-table-action" title="Editar" onclick="editAdmin(${admin.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-table-action delete-action" title="Eliminar" onclick="deleteAdmin(${admin.id})">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        document.getElementById('pagination-status-text').innerText = `Mostrando ${admins.length} de ${admins.length} administradores`;
    }

    // Modal helpers
    function openAdminModal() {
        document.getElementById('modal-title').innerText = 'Añadir Administrador';
        document.getElementById('admin-id').value = '';
        document.getElementById('admin-name').value = '';
        document.getElementById('admin-email').value = '';
        document.getElementById('admin-role').value = '';
        document.getElementById('admin-sector').value = 'Hoteles';
        document.getElementById('admin-status').value = 'Conectado';
        
        document.getElementById('admin-modal').classList.add('show');
    }

    function closeAdminModal() {
        document.getElementById('admin-modal').classList.remove('show');
    }

    function saveAdmin() {
        const id = document.getElementById('admin-id').value;
        const name = document.getElementById('admin-name').value.trim();
        const email = document.getElementById('admin-email').value.trim();
        const sector = document.getElementById('admin-sector').value;
        const role = document.getElementById('admin-role').value.trim();
        const status = document.getElementById('admin-status').value;

        if(!name || !email || !role) {
            alert('Por favor completa todos los campos obligatorios');
            return;
        }

        if(id) {
            // Editar
            const index = admins.findIndex(a => a.id == id);
            if(index !== -1) {
                admins[index] = { id: parseInt(id), name, email, sector, role, status };
                showToast(`Administrador "${name}" actualizado con éxito`);
            }
        } else {
            // Añadir
            const newId = admins.length > 0 ? Math.max(...admins.map(a => a.id)) + 1 : 1;
            admins.push({ id: newId, name, email, sector, role, status });
            showToast(`Nuevo administrador "${name}" creado con éxito`);
        }

        closeAdminModal();
        renderAdminsTable();
    }

    function editAdmin(id) {
        const admin = admins.find(a => a.id == id);
        if(!admin) return;

        document.getElementById('modal-title').innerText = 'Editar Administrador';
        document.getElementById('admin-id').value = admin.id;
        document.getElementById('admin-name').value = admin.name;
        document.getElementById('admin-email').value = admin.email;
        document.getElementById('admin-role').value = admin.role;
        document.getElementById('admin-sector').value = admin.sector;
        document.getElementById('admin-status').value = admin.status;

        document.getElementById('admin-modal').classList.add('show');
    }

    function deleteAdmin(id) {
        const admin = admins.find(a => a.id == id);
        if(!admin) return;

        if(confirm(`¿Estás seguro de que deseas eliminar al administrador "${admin.name}"?`)) {
            const row = document.getElementById(`admin-row-${id}`);
            row.style.transition = 'all 0.4s ease';
            row.style.opacity = '0';
            row.style.transform = 'translateY(-15px)';

            setTimeout(() => {
                admins = admins.filter(a => a.id != id);
                renderAdminsTable();
                showToast(`Administrador "${admin.name}" eliminado de YÚMANO`);
            }, 400);
        }
    }

    // 2. BUSCADOR/FILTRADO DE EVENTOS EN TIEMPO REAL
    document.getElementById('filter-activities-input').addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase().trim();
        const items = document.querySelectorAll('.activity-item-heritage');

        items.forEach(item => {
            const matchText = item.getAttribute('data-text');
            if(matchText.includes(query)) {
                item.style.display = 'flex';
                item.classList.add('animate-fade-in');
            } else {
                item.style.display = 'none';
            }
        });
    });

    // 3. TOAST NOTIFICATIONS
    function showToast(message) {
        const container = document.getElementById('toast-container');
        
        const toast = document.createElement('div');
        toast.className = 'toast-heritage';
        toast.innerHTML = `
            <i class="fas fa-check-circle toast-heritage-icon"></i>
            <span>${message}</span>
            <button class="toast-heritage-close" onclick="this.parentElement.remove()">&times;</button>
        `;
        
        container.appendChild(toast);
        
        // Trigger reflow & show
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    }

    // 4. RESOLVER ALERTAS CON ANIMACIÓN
    function resolveAlert(id, successMsg) {
        const alertCard = document.getElementById(id);
        if(!alertCard) return;

        alertCard.style.transition = 'all 0.4s ease';
        alertCard.style.opacity = '0';
        alertCard.style.transform = 'translateX(-30px)';

        setTimeout(() => {
            alertCard.remove();
            showToast(successMsg);
            
            // Si no quedan alertas, mostrar un mensaje por defecto
            const container = document.getElementById('alerts-container');
            if(container.children.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-4 text-secondary">
                        <i class="fas fa-heart fa-2x text-success opacity-50 mb-2"></i>
                        <p class="mb-0">¡Salud del Ecosistema al 100%! No hay alertas pendientes.</p>
                    </div>
                `;
            }
        }, 400);
    }

    // 5. NAVEGACIÓN ENTRE PESTAÑAS (SIDEBAR)
    document.querySelectorAll('.sidebar-link[data-target]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active classes
            document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
            document.querySelectorAll('.dashboard-pane').forEach(p => p.classList.remove('active'));

            // Add active class
            this.classList.add('active');
            const targetId = this.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    function switchPane(targetId) {
        document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.dashboard-pane').forEach(p => p.classList.remove('active'));

        const sidebarLink = document.querySelector(`.sidebar-link[data-target="${targetId}"]`);
        if(sidebarLink) sidebarLink.classList.add('active');
        document.getElementById(targetId).classList.add('active');
    }

    // 6. CONTROL DE GRÁFICOS (BARRAS / LÍNEAS)
    document.getElementById('btn-chart-bar').addEventListener('click', function() {
        this.classList.add('active');
        document.getElementById('btn-chart-line').classList.remove('active');
        
        document.getElementById('chart-bars').classList.remove('chart-hidden');
        document.getElementById('chart-lines').classList.add('chart-hidden');
    });

    document.getElementById('btn-chart-line').addEventListener('click', function() {
        this.classList.add('active');
        document.getElementById('btn-chart-bar').classList.remove('active');
        
        document.getElementById('chart-lines').classList.remove('chart-hidden');
        document.getElementById('chart-bars').classList.add('chart-hidden');
    });

    // 7. CONMUTACIÓN DE MODO OSCURO (LOCALSTORAGE Y ATRIBUTOS)
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-bs-theme', nextTheme);
        localStorage.setItem('theme', nextTheme);
        
        // Actualizar icono
        const themeIcon = document.getElementById('theme-toggle-icon');
        if (nextTheme === 'dark') {
            themeIcon.className = 'fas fa-sun';
            showToast('Modo Oscuro activado');
        } else {
            themeIcon.className = 'fas fa-moon';
            showToast('Modo Claro activado');
        }
    }

    // Inicializar icono en base al tema guardado al cargar
    function initThemeIcon() {
        const theme = document.documentElement.getAttribute('data-bs-theme') || 'light';
        const themeIcon = document.getElementById('theme-toggle-icon');
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
        } else {
            themeIcon.className = 'fas fa-moon';
        }
    }

    // 8. MENÚ HAMBURGUESA MÓVIL
    function toggleSidebar() {
        document.getElementById('sidebar').classList.toggle('open');
    }

    function closeSidebarOnMobile() {
        if(window.innerWidth <= 992) {
            document.getElementById('sidebar').classList.remove('open');
        }
    }

    // Cerrar sidebar clicando fuera
    document.addEventListener('click', function(e) {
        const sidebar = document.getElementById('sidebar');
        const toggleBtn = document.getElementById('sidebar-toggle-btn');
        if (window.innerWidth <= 992 && sidebar.classList.contains('open')) {
            if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    });

    // 9. GENERACIÓN Y DESCARGA DE REPORTE CSV INTERACTIVO
    function downloadConsolidatedReport() {
        // Encabezado del CSV con BOM para soporte UTF-8 en Excel en español
        let csvContent = "data:text/csv;charset=utf-8,\uFEFF";
        
        csvContent += "========================================================\n";
        csvContent += "REPORTE CONSOLIDADO - CENTRO DE CONTROL YÚMANO\n";
        csvContent += "Generado el: " + new Date().toLocaleString() + "\n";
        csvContent += "========================================================\n\n";
        
        // 1. Salud del Ecosistema
        csvContent += "1. SALUD DEL ECOSISTEMA\n";
        csvContent += "Sector,Ingresos Registrados,Activos Registrados\n";
        csvContent += `Hoteles,$45.2M COP,${document.getElementById('hotels-count').innerText.split(' ')[0]} activos\n`;
        csvContent += "Gastronomía,$28.9M COP,{{ dashboard_data.gastronomias_totales }} activos\n";
        csvContent += "Tiendas,$12.4M COP,{{ dashboard_data.productos_totales }} productos activos\n";
        csvContent += "Experiencias,$19.7M COP,{{ dashboard_data.experiencias_totales }} experiencias activas\n";
        csvContent += "Servicios,$8.1M COP,{{ dashboard_data.servicios_totales }} servicios activos\n\n";
        
        // 2. Administradores
        csvContent += "2. CONTROL DE ADMINISTRADORES REGISTRADOS\n";
        csvContent += "Nombre,Correo,Sector Asignado,Rol del Cargo,Estado Actual\n";
        admins.forEach(admin => {
            csvContent += `"${admin.name}","${admin.email}","${admin.sector}","${admin.role}","${admin.status}"\n`;
        });
        csvContent += "\n";
        
        // 3. Actividad Reciente
        csvContent += "3. REGISTRO DE LOGS DE ACTIVIDAD RECIENTE\n";
        csvContent += "Hora,Actividad,Detalle del Evento\n";
        csvContent += "14:22,Nueva Reserva VIP,Experiencia 'Ruta del Cacao' para 4 personas (Faiver Bravo).\n";
        csvContent += "13:05,Actualización de Precios,Sector Tiendas actualizó tarifas de temporada (Artesanías Agustín).\n";
        csvContent += "11:46,Alta de Colaborador,Elena M. asignada a Guías de Montaña.\n";
        
        // Crear elemento de descarga e iniciar
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `reporte_consolidado_yumano_${new Date().toISOString().slice(0, 10)}.csv`);
        document.body.appendChild(link);
        
        link.click();
        document.body.removeChild(link);
        
        showToast("Reporte consolidado descargado en formato CSV");
    }

    // Carga inicial de datos de la tabla e inicio de tema
    window.addEventListener('DOMContentLoaded', () => {
        renderAdminsTable();
        initThemeIcon();
    });
