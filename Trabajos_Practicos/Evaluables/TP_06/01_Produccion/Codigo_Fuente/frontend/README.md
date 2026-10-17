# EcoHarmony Park — Frontend Ionic

Aplicación web responsive construida con React, TypeScript, Ionic y Vite.

## Requisitos

- Node.js LTS
- npm

## Ejecutar en desarrollo

```bash
npm ci
npm run dev
```

## Pruebas y compilación

```bash
npm test
npm run build
```

## Estilo visual

- Fuente Lato incluida localmente mediante `@fontsource/lato`.
- Paleta del PO: `#386641`, `#6a994e`, `#a7c957`, `#f2e8cf`, `#bc4749`.
- Fondo fotográfico del parque con movimiento lento, hero animado y superficies translúcidas.
- Estados hover/focus/active en botones, tarjetas y navegación.
- Diseño responsive y respeto por `prefers-reduced-motion` para reducir animaciones si el sistema lo solicita.
- Se conserva la navegación Ionic y las pantallas/funcionalidades existentes.

## Simulación local

El archivo `.env.local` de esta entrega configura `VITE_API_MOCK=true` para permitir probar el flujo simulado sin depender del backend. No se realizan cobros ni se envían correos reales.
