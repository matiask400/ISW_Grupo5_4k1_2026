import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

const BACKEND_DEV_URL = 'http://localhost:8000';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: 'auto',
      includeAssets: ['icons/apple-touch-icon.png'],
      manifest: {
        name: 'EcoHarmony Park',
        short_name: 'EcoHarmony',
        description: 'Página web de EcoHarmony Park',
        lang: 'es',
        start_url: '/',
        scope: '/',
        display: 'standalone',
        orientation: 'portrait-primary',
        background_color: '#ffffff',
        theme_color: '#386641',
        icons: [
          { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
          {
            src: '/icons/icon-maskable-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,png,jpg,svg,ico,woff2}'],
        maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
        // La app es una SPA: cualquier ruta de navegación sirve index.html,
        // excepto las llamadas a la API, que siempre van al servidor.
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api\//],
      },
    }),
  ],
  // El backend espera el front en el puerto 5173: es el origen permitido por
  // CORS y el que usa la URL de retorno de Mercado Pago (/compra-finalizada).
  preview: {
    port: 5173,
    strictPort: true,
  },
  server: {
    port: 5173,
    strictPort: true,
    // En desarrollo, todo lo que empiece con /api se reenvía al backend.
    // Así no hace falta configurar CORS en FastAPI mientras desarrollás.
    proxy: {
      '/api': { target: BACKEND_DEV_URL, changeOrigin: true },
    },
  },
});
