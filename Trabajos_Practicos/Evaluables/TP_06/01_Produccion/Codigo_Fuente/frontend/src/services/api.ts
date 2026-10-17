// Comunicación con el backend.
//
// En desarrollo VITE_API_URL queda vacío y las rutas /api/... pasan por el
// proxy de Vite (vite.config.ts). En producción se define en el archivo .env.
// Contrato: backend/app/api/rutas_compras.py y esquemas.py.

import { calcularTotalEntradas, validarLimiteAcumuladoEntradas } from './reglasCompra';
import type { ResultadoCompra, SolicitudCompra } from './tipos';

const API_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '');
const API_MOCK = import.meta.env.VITE_API_MOCK === 'true';

/** Endpoint acordado con backend para registrar la compra. */
export const ENDPOINT_COMPRAS = '/api/compras';

/** Header con el que el backend identifica al usuario (sesión simulada). */
export const HEADER_USUARIO = 'X-Usuario-Email';

export async function comprarEntradas(solicitud: SolicitudCompra): Promise<ResultadoCompra> {
  if (API_MOCK) return simularCompra(solicitud);

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

/** Implementación temporal del contrato de compra, activada por VITE_API_MOCK=true. */
async function simularCompra(solicitud: SolicitudCompra): Promise<ResultadoCompra> {
  // Simula latencia de red sin depender del backend.
  await new Promise((resolve) => setTimeout(resolve, 350));
  const tipoPase = solicitud.tipo_pase ?? 'REGULAR';
  const comprasPrevias = leerEntradasMock(solicitud.usuario_email, solicitud.fecha_visita);
  const errorLimite = validarLimiteAcumuladoEntradas(comprasPrevias, solicitud.cantidad);
  if (errorLimite) return { exitosa: false, error: errorLimite };

  const total = calcularTotalEntradas(tipoPase, solicitud.edades);
  const numeroOrden = `EHP-${Date.now().toString().slice(-8)}`;
  const resultado: ResultadoCompra = {
    exitosa: true,
    cantidad: solicitud.cantidad,
    fecha_visita: solicitud.fecha_visita,
    monto_total: total,
    mensaje: `${solicitud.cantidad} entrada(s) para el ${solicitud.fecha_visita}. Total: ${new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 }).format(total)}.`,
    mail_enviado_a: solicitud.usuario_email,
    numero_orden: numeroOrden,
    detalle_visitantes: solicitud.edades.map((edad) => ({
      edad,
      subtotal: calcularTotalEntradas(tipoPase, [edad]),
    })),
    adjunto_nombre: `Entradas_${numeroOrden}.pdf`,
  };

  if (solicitud.forma_pago === 'TARJETA') {
    resultado.url_pago = `/mercado-pago-simulado?monto=${total}`;
  }
  guardarEntradasMock(solicitud.usuario_email, solicitud.fecha_visita, comprasPrevias + solicitud.cantidad);
  return resultado;
}

const CLAVE_COMPRAS_MOCK = 'ecoharmony:entradas-mock';

function leerEntradasMock(email: string, fecha: string): number {
  try {
    const compras = JSON.parse(localStorage.getItem(CLAVE_COMPRAS_MOCK) ?? '{}') as Record<string, number>;
    return compras[`${email.toLowerCase()}:${fecha}`] ?? 0;
  } catch {
    return 0;
  }
}

function guardarEntradasMock(email: string, fecha: string, cantidad: number): void {
  try {
    const compras = JSON.parse(localStorage.getItem(CLAVE_COMPRAS_MOCK) ?? '{}') as Record<string, number>;
    compras[`${email.toLowerCase()}:${fecha}`] = cantidad;
    localStorage.setItem(CLAVE_COMPRAS_MOCK, JSON.stringify(compras));
  } catch {
    // El modo mock sigue siendo utilizable si el navegador bloquea el almacenamiento.
  }
}

