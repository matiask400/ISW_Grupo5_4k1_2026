export type TipoPase = 'REGULAR' | 'VIP';
export type FormaPago = 'EFECTIVO' | 'TARJETA';

export interface SolicitudCompra {
  usuario_email: string;
  fecha_visita: string; // formato ISO "YYYY-MM-DD"
  cantidad: number;
  edades: number[];
  tipo_pase: TipoPase | null;
  forma_pago: FormaPago | null;
}

export interface ResultadoCompra {
  exitosa: boolean;
  error?: string | null;
  cantidad?: number | null;
  fecha_visita?: string | null;
  monto_total?: number | null;
  mensaje?: string | null;
  url_pago?: string | null;
  mail_enviado_a?: string | null;
}
