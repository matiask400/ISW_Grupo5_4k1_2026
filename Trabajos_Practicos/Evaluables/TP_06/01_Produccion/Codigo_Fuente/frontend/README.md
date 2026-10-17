# Eco Harmony Park — Frontend

Frontend responsive construido con React, TypeScript, Ionic y Vite.

## Ejecutar localmente

```bash
npm ci
npm run dev
```

## Pruebas y build

```bash
npm test
npm run build
```

## Modo de integración

- `VITE_API_MOCK=true`: simula la compra en el frontend, registra el límite acumulado de entradas por usuario/fecha en `localStorage`, genera un número de orden y muestra la pasarela y el correo simulados. No se envía dinero ni correo real.
- `VITE_API_MOCK=false`: usa `POST /api/compras` y el contrato definido en `src/services/api.ts`.
- `VITE_API_URL`: URL base opcional del backend. Si queda vacía, las rutas `/api/...` usan el proxy configurado en Vite.

La configuración local está en `.env.local` (no se versiona). `.env.example` documenta las variables disponibles.

## TDD

Los cambios recientes están organizados en commits de pruebas y desarrollo (`test(RED)`, `feat(GREEN)` y `refactor`). Las reglas de precio y del límite acumulado tienen pruebas en `src/services/reglasCompra.test.ts`.