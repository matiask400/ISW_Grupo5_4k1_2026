// Comunicación con el backend.
//
// En desarrollo VITE_API_URL queda vacío y las rutas /api/... pasan por el
// proxy de Vite (vite.config.ts). En producción se define en el archivo .env.
// Contrato: backend/app/api/rutas_compras.py y esquemas.py.

import type { ResultadoCompra, SolicitudCompra } from './tipos';

const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '');

/** Endpoint acordado con backend para registrar la compra. */
export const ENDPOINT_COMPRAS = '/api/compras';

/** Header con el que el backend identifica al usuario (sesión simulada). */
export const HEADER_USUARIO = 'X-Usuario-Email';

export async function comprarEntradas(solicitud: SolicitudCompra): Promise<ResultadoCompra> {
  const { usuario_email, ...pedido } = solicitud;
  let respuesta: Response;
  try {
    respuesta = await fetch(`${API_URL}${ENDPOINT_COMPRAS}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', [HEADER_USUARIO]: usuario_email },
      body: JSON.stringify(pedido),
    });
  } catch {
    return {
      exitosa: false,
      error: 'No se pudo conectar con el servidor. Revisá tu conexión e intentá de nuevo.',
    };
  }

  const datos: unknown = await respuesta.json().catch(() => null);

  // Compra exitosa (201): RespuestaCompra con mensaje, monto, url_pago, etc.
  if (respuesta.ok && datos && typeof datos === 'object' && 'exitosa' in datos) {
    return datos as ResultadoCompra;
  }
  // Errores de negocio (401, 403, 422) traen { detail: "mensaje" }.
  // Los de validación automática de FastAPI traen { detail: [ ... ] }.
  if (datos && typeof datos === 'object' && 'detail' in datos) {
    const detalle = (datos as { detail: unknown }).detail;
    if (typeof detalle === 'string') return { exitosa: false, error: detalle };
    if (Array.isArray(detalle)) {
      return { exitosa: false, error: 'Los datos de la compra no son válidos. Revisalos.' };
    }
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
