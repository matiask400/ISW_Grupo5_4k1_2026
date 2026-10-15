const CACHE_NAME = 'pwa-cache-v1';

self.addEventListener('install', (event) => {
  console.log('[SW] Instalado');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('[SW] Activado');
  return self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Por ahora dejamos pasar las peticiones a la red directamente
  event.respondWith(fetch(event.request));
});