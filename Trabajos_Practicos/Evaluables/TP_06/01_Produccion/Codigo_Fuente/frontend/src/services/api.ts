
import type { ResultadoCompra, SolicitudCompra } from './tipos';

const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '');


export const ENDPOINT_COMPRAS = '/api/compras';
export const ENDPOINT_CONFIRMAR_PAGO = '/api/compras/confirmar-pago';
export const HEADER_USUARIO = 'X-Usuario-Email';

export async function comprarEntradas(solicitud: SolicitudCompra): Promise<ResultadoCompra> {
  const { usuario_email, ...pedido } = solicitud;
  return enviar(ENDPOINT_COMPRAS, usuario_email, pedido);
}

export async function confirmarPago(
  paymentId: string,
  usuarioEmail: string,
): Promise<ResultadoCompra> {
  return enviar(ENDPOINT_CONFIRMAR_PAGO, usuarioEmail, { payment_id: paymentId });
}

async function enviar(
  endpoint: string,
  usuarioEmail: string,
  cuerpo: unknown,
): Promise<ResultadoCompra> {
  let respuesta: Response;
  try {
    respuesta = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', [HEADER_USUARIO]: usuarioEmail },
      body: JSON.stringify(cuerpo),
    });
  } catch {
    return {
      exitosa: false,
      error: 'No se pudo conectar con el servidor. Revisá tu conexión e intentá de nuevo.',
    };
  }

  const datos: unknown = await respuesta.json().catch(() => null);

  if (respuesta.ok && datos && typeof datos === 'object' && 'exitosa' in datos) {
    return datos as ResultadoCompra;
  }

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
