// Comunicación con el backend.
//
// En desarrollo VITE_API_URL queda vacío y las rutas /api/... pasan por el
// proxy de Vite (vite.config.ts). En producción se define en el archivo .env.

import type { ResultadoCompra, SolicitudCompra } from './tipos';

const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '');

/** Endpoint acordado con backend para registrar la compra. */
export const ENDPOINT_COMPRAS = '/api/compras';

export async function comprarEntradas(solicitud: SolicitudCompra): Promise<ResultadoCompra> {
  let respuesta: Response;
  try {
    respuesta = await fetch(`${API_URL}${ENDPOINT_COMPRAS}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(solicitud),
    });
  } catch {
    return {
      exitosa: false,
      error: 'No se pudo conectar con el servidor. Revisá tu conexión e intentá de nuevo.',
    };
  }

  const datos: unknown = await respuesta.json().catch(() => null);

  // El backend responde con un ResultadoCompra: { exitosa, error }
  if (datos && typeof datos === 'object' && 'exitosa' in datos) {
    return datos as ResultadoCompra;
  }
  // Errores de validación automáticos de FastAPI (422) traen "detail"
  if (datos && typeof datos === 'object' && 'detail' in datos) {
    const detalle = (datos as { detail: unknown }).detail;
    if (typeof detalle === 'string') return { exitosa: false, error: detalle };
  }
  if (respuesta.status === 404) {
    return {
      exitosa: false,
      error: 'El servidor todavía no tiene habilitada la compra de entradas.',
    };
  }
  return {
    exitosa: false,
    error: `El servidor respondió con un error (${respuesta.status}). Intentá más tarde.`,
  };
}
