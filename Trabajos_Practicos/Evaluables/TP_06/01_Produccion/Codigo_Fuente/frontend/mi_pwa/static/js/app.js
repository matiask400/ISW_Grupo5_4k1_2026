let deferredPrompt = null;
const installBanner = document.getElementById('install-banner');
const btnInstall = document.getElementById('btn-install');
const networkBadge = document.getElementById('network-badge');
const btnFetch = document.getElementById('btn-fetch');
const apiOutput = document.getElementById('api-output');

// Referencias a los botones de navegación y a las pantallas
const navInicio = document.getElementById('nav-inicio');
const navGestion = document.getElementById('nav-gestion');
const viewInicio = document.getElementById('view-inicio');
const viewGestion = document.getElementById('view-gestion');

function mostrarPantalla(vistaAMostrar) {
  // Ocultamos todas las vistas
  viewInicio.classList.add('hidden');
  viewInicio.classList.remove('active');
  viewGestion.classList.add('hidden');
  viewGestion.classList.remove('active');

  // Mostramos solo la seleccionada
  vistaAMostrar.classList.remove('hidden');
  vistaAMostrar.classList.add('active');
}

// Eventos de navegación
navInicio.addEventListener('click', () => mostrarPantalla(viewInicio));
navGestion.addEventListener('click', () => mostrarPantalla(viewGestion));

// 1. Registro del Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const reg = await navigator.serviceWorker.register('/sw.js');
      console.log('[PWA] Service Worker activo:', reg.scope);
    } catch (err) {
      console.error('[PWA] Error en Service Worker:', err);
    }
  });
}

// 2. Evento para capturar el prompt de instalación (PWA installable)
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBanner.style.display = 'block'; // Mostramos el botón
});

btnInstall.addEventListener('click', async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const choiceResult = await deferredPrompt.userChoice;
  if (choiceResult.outcome === 'accepted') {
    console.log('[PWA] Usuario aceptó instalar la app');
  }
  deferredPrompt = null;
  installBanner.style.display = 'none';
});

// 3. Monitoreo de estado de conexión (Online / Offline)
function updateNetworkStatus() {
  if (navigator.onLine) {
    networkBadge.textContent = 'En línea';
    networkBadge.className = 'badge online';
  } else {
    networkBadge.textContent = 'Sin conexión';
    networkBadge.className = 'badge offline';
  }
}
window.addEventListener('online', updateNetworkStatus);
window.addEventListener('offline', updateNetworkStatus);
updateNetworkStatus();

// 4. Consulta a la API con manejo de fallos
btnFetch.addEventListener('click', async () => {
  apiOutput.textContent = 'Consultando endpoint...';
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    apiOutput.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    apiOutput.textContent = 'Error: no se pudo conectar con el servidor (posiblemente offline).';
  }
});

const btnMenu = document.getElementById('btn-menu');
const btnCloseMenu = document.getElementById('btn-close-menu');
const sideMenu = document.getElementById('side-menu');
const menuOverlay = document.getElementById('menu-overlay');

function toggleMenu(abrir) {
  if (abrir) {
    sideMenu.classList.add('open');
    menuOverlay.classList.add('active');
  } else {
    sideMenu.classList.remove('open');
    menuOverlay.classList.remove('active');
  }
}

// Eventos de apertura y cierre
btnMenu.addEventListener('click', () => toggleMenu(true));
btnCloseMenu.addEventListener('click', () => toggleMenu(false));
menuOverlay.addEventListener('click', () => toggleMenu(false));

// Cerrar el menú al hacer clic en cualquier opción
document.querySelectorAll('.side-menu a').forEach(enlace => {
  enlace.addEventListener('click', () => {
    toggleMenu(false);
  });
});