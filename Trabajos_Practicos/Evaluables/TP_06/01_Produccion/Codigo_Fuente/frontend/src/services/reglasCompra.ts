
import type { SolicitudCompra, TipoPase } from './tipos';

export const MINIMO_ENTRADAS_POR_COMPRA = 1;
export const MAXIMO_ENTRADAS_POR_COMPRA = 10;
export const EDAD_MINIMA = 0;
export const EDAD_MAXIMA = 120;
export const HORA_LIMITE_COMPRA_MISMO_DIA = { horas: 17, minutos: 30 };

const MAXIMO_DIGITOS_EDAD = String(EDAD_MAXIMA).length;


export function soloDigitosEdad(texto: string): string {
  return texto.replace(/\D/g, '').slice(0, MAXIMO_DIGITOS_EDAD);
}


export const PRECIOS_PASE: Record<TipoPase, number> = {
  REGULAR: 10_000,
  VIP: 20_000,
};


export function calcularPrecioEntrada(tipoPase: TipoPase, edad: number): number {
  if (edad <= 3) return 0;
  if (edad <= 15 || edad >= 60) return PRECIOS_PASE[tipoPase] * 0.5;
  return PRECIOS_PASE[tipoPase];
}


export function calcularTotalEntradas(tipoPase: TipoPase, edades: number[]): number {
  return edades.reduce((total, edad) => total + calcularPrecioEntrada(tipoPase, edad), 0);
}


export function validarLimiteAcumuladoEntradas(compradas: number, nuevas: number): string | null {
  return compradas + nuevas > MAXIMO_ENTRADAS_POR_COMPRA
    ? `Solo podés comprar hasta ${MAXIMO_ENTRADAS_POR_COMPRA} entradas para una misma fecha`
    : null;
}


const FERIADOS_CERRADO: Array<[number, number]> = [
  [12, 25],
  [1, 1],
];


export interface Fecha {
  anio: number;
  mes: number;
  dia: number;
}

export function fechaDesdeDate(d: Date): Fecha {
  return { anio: d.getFullYear(), mes: d.getMonth() + 1, dia: d.getDate() };
}

export function fechaDesdeIso(iso: string): Fecha {
  const [anio, mes, dia] = iso.slice(0, 10).split('-').map(Number);
  return { anio, mes, dia };
}

export function fechaAIso(f: Fecha): string {
  const dos = (n: number) => String(n).padStart(2, '0');
  return `${f.anio}-${dos(f.mes)}-${dos(f.dia)}`;
}

function compararFechas(a: Fecha, b: Fecha): number {
  return a.anio - b.anio || a.mes - b.mes || a.dia - b.dia;
}

function diasDelMes(anio: number, mes: number): number {
  return new Date(anio, mes, 0).getDate();
}


export function sumarUnMes(f: Fecha): Fecha {
  const anio = f.mes === 12 ? f.anio + 1 : f.anio;
  const mes = f.mes === 12 ? 1 : f.mes + 1;
  return { anio, mes, dia: Math.min(f.dia, diasDelMes(anio, mes)) };
}


export function parqueAbierto(f: Fecha): boolean {
  const esLunes = new Date(f.anio, f.mes - 1, f.dia).getDay() === 1;
  const esFeriado = FERIADOS_CERRADO.some(([m, d]) => m === f.mes && d === f.dia);
  return !esLunes && !esFeriado;
}

function pasoHoraLimite(ahora: Date): boolean {
  const { horas, minutos } = HORA_LIMITE_COMPRA_MISMO_DIA;
  const segundos = ahora.getHours() * 3600 + ahora.getMinutes() * 60 + ahora.getSeconds();
  return segundos > horas * 3600 + minutos * 60;
}


export function rangoFechasPermitidas(ahora: Date = new Date()) {
  const hoy = fechaDesdeDate(ahora);
  return { min: fechaAIso(hoy), max: fechaAIso(sumarUnMes(hoy)) };
}

export function fechaSeleccionable(iso: string, ahora: Date = new Date()): boolean {
  const fecha = fechaDesdeIso(iso);
  const esHoy = compararFechas(fecha, fechaDesdeDate(ahora)) === 0;
  if (esHoy && pasoHoraLimite(ahora)) return false;
  return parqueAbierto(fecha);
}


function validarFecha(s: SolicitudCompra, ahora: Date): string | null {
  if (!s.fecha_visita) return 'Debe seleccionar una fecha de visita';
  const hoy = fechaDesdeDate(ahora);
  const fecha = fechaDesdeIso(s.fecha_visita);

  if (compararFechas(fecha, hoy) < 0) {
    return 'La fecha de visita debe ser hoy o una fecha futura';
  }
  if (compararFechas(fecha, sumarUnMes(hoy)) > 0) {
    return 'Solo se pueden comprar entradas con hasta 1 mes de anticipación';
  }
  if (compararFechas(fecha, hoy) === 0 && pasoHoraLimite(ahora)) {
    const { horas, minutos } = HORA_LIMITE_COMPRA_MISMO_DIA;
    const limite = `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}`;
    return `Las compras para el día de hoy se permiten hasta las ${limite}`;
  }
  if (!parqueAbierto(fecha)) {
    return 'El parque está cerrado en la fecha seleccionada';
  }
  return null;
}

function validarCantidad(s: SolicitudCompra): string | null {
  if (s.cantidad < MINIMO_ENTRADAS_POR_COMPRA) return 'Debe comprar al menos 1 entrada';
  if (s.cantidad > MAXIMO_ENTRADAS_POR_COMPRA) {
    return `La cantidad de entradas no puede superar ${MAXIMO_ENTRADAS_POR_COMPRA}`;
  }
  return null;
}

function validarVisitantes(s: SolicitudCompra): string | null {
  if (s.edades.length !== s.cantidad || s.edades.some((e) => !Number.isInteger(e))) {
    return 'Debe indicar la edad de cada visitante';
  }
  if (s.edades.some((e) => e < EDAD_MINIMA || e > EDAD_MAXIMA)) {
    return `Las edades deben estar entre ${EDAD_MINIMA} y ${EDAD_MAXIMA}`;
  }
  return null;
}

function validarTipoPase(s: SolicitudCompra): string | null {
  return s.tipo_pase === null ? 'Debe seleccionar un tipo de pase' : null;
}

function validarFormaPago(s: SolicitudCompra): string | null {
  return s.forma_pago === null ? 'Debe seleccionar una forma de pago' : null;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


function validarEmail(s: SolicitudCompra): string | null {
  return EMAIL_REGEX.test(s.usuario_email.trim()) ? null : 'Ingresá un email válido';
}

export function validarSolicitud(s: SolicitudCompra, ahora: Date = new Date()): string | null {
  return (
    validarEmail(s) ??
    validarFecha(s, ahora) ??
    validarCantidad(s) ??
    validarVisitantes(s) ??
    validarTipoPase(s) ??
    validarFormaPago(s)
  );
}
