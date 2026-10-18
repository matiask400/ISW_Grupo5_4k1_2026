// Tipos que reflejan los modelos del backend (backend/app/modelos/modelos.py).
// Los nombres de campos están en snake_case para que el JSON coincida 1 a 1.

export type TipoPase = 'REGULAR' | 'VIP';
export type FormaPago = 'EFECTIVO' | 'TARJETA';

export interface SolicitudCompra {
  usuario_email: string; // viaja en el header X-Usuario-Email, no en el cuerpo
  fecha_visita: string; // formato ISO "YYYY-MM-DD"
  cantidad: number;
  edades: number[];
  tipo_pase: TipoPase | null;
  forma_pago: FormaPago | null;
}

/** Refleja RespuestaCompra de backend/app/api/esquemas.py. */
export interface ResultadoCompra {
  exitosa: boolean;
  error?: string | null;
  cantidad?: number | null;
  fecha_visita?: string | null;
  monto_total?: number | null;
  mensaje?: string | null;
  url_pago?: string | null; // solo con TARJETA: checkout de Mercado Pago
  mail_enviado_a?: string | null;
}
