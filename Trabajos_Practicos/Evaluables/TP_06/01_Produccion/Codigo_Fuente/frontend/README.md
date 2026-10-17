# EcoHarmony Park — Frontend

Aplicación frontend desarrollada con React, TypeScript, Ionic y Vite.

## Ejecutar localmente

```bash
npm ci
npm run dev
```

## Pruebas y compilación

```bash
npm test
npm run build
```

## Interfaz

- Identidad visual basada en la paleta `#386641`, `#6a994e`, `#a7c957`, `#f2e8cf`, `#bc4749` y tipografía Lato.
- Portada con hero fotográfico, degradado, zoom lento, aparición suave del contenido y CTA principales.
- Secciones de beneficios, galería ilustrativa, horarios, datos de ubicación pendientes de confirmar, recomendaciones familiares, preguntas frecuentes y testimonios claramente rotulados como demostración.
- Compra con indicador de pasos, calendario, selector de cantidad, edades por visitante, cálculo de descuentos, resumen lateral y estados de validación/procesamiento.
- Animaciones con soporte para `prefers-reduced-motion`.

## Datos y demostración

La ubicación exacta del parque todavía no está configurada en la interfaz. Las fotografías externas son ilustrativas y los testimonios están identificados como ejemplos, no como opiniones reales. La integración de pago y correo sigue el comportamiento simulado/implementado por el proyecto.

Para habilitar el modo mock local, revisar la variable `VITE_API_MOCK` en `.env.local` según el entorno de desarrollo.
