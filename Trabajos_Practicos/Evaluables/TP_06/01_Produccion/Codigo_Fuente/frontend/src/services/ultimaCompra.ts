// Guarda la última compra registrada para confirmarla después de pasar por
// Mercado Pago (la redirección recarga la app y se pierde el estado de React).

import type { ResultadoCompra } from './tipos';

const CLAVE = 'ecoharmony:ultima-compra';

export interface UltimaCompra {
  usuario_email: string;
  resultado: ResultadoCompra;
}

export function guardarUltimaCompra(usuarioEmail: string, resultado: ResultadoCompra): void {
  const compra: UltimaCompra = { usuario_email: usuarioEmail, resultado };
  sessionStorage.setItem(CLAVE, JSON.stringify(compra));
}

export function leerUltimaCompra(): UltimaCompra | null {
  try {
    return JSON.parse(sessionStorage.getItem(CLAVE) ?? 'null') as UltimaCompra | null;
  } catch {
    return null;
  }
}
