// Guarda la última compra confirmada para mostrarla después de pasar por
// Mercado Pago (la redirección recarga la app y se pierde el estado de React).

import type { ResultadoCompra } from './tipos';

const CLAVE = 'ecoharmony:ultima-compra';

export function guardarUltimaCompra(resultado: ResultadoCompra): void {
  sessionStorage.setItem(CLAVE, JSON.stringify(resultado));
}

export function leerUltimaCompra(): ResultadoCompra | null {
  try {
    return JSON.parse(sessionStorage.getItem(CLAVE) ?? 'null') as ResultadoCompra | null;
  } catch {
    return null;
  }
}
