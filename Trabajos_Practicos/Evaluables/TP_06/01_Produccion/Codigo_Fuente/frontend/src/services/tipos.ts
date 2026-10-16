// Tipos que reflejan los modelos del backend (backend/app/modelos/modelos.py).
// Los nombres de campos están en snake_case para que el JSON coincida 1 a 1.

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
}
