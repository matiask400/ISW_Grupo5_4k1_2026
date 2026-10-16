import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// El service worker de la PWA lo registra vite-plugin-pwa automáticamente.
createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
