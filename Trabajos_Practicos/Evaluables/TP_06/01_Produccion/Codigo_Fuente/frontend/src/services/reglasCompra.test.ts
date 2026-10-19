import { describe, expect, it } from 'vitest';
import {
  calcularPrecioEntrada,
  calcularTotalEntradas,
  validarLimiteAcumuladoEntradas,
  fechaSeleccionable,
  rangoFechasPermitidas,
  soloDigitosEdad,
  sumarUnMes,
  validarSolicitud,
} from './reglasCompra';
import type { SolicitudCompra } from './tipos';

const AHORA = new Date(2026, 9, 22, 10, 0); // 22/10/2026 10:00 (jueves)

function solicitud(cambios: Partial<SolicitudCompra> = {}): SolicitudCompra {
  return {
    usuario_email: 'ana@mail.com',
    fecha_visita: '2026-10-29',
    cantidad: 2,
    edades: [30, 25],
    tipo_pase: 'REGULAR',
    forma_pago: 'EFECTIVO',
    ...cambios,
  };
}

describe('validarSolicitud', () => {
  it('acepta una compra válida', () => {
    expect(validarSolicitud(solicitud(), AHORA)).toBeNull();
  });

  it('no permite más de 10 entradas', () => {
    const s = solicitud({ cantidad: 11, edades: Array(11).fill(30) });
    expect(validarSolicitud(s, AHORA)).toBe('La cantidad de entradas no puede superar 10');
  });

  it('exige al menos 1 entrada', () => {
    const s = solicitud({ cantidad: 0, edades: [] });
    expect(validarSolicitud(s, AHORA)).toBe('Debe comprar al menos 1 entrada');
  });

  it('exige forma de pago', () => {
    expect(validarSolicitud(solicitud({ forma_pago: null }), AHORA)).toBe(
      'Debe seleccionar una forma de pago',
    );
  });

  it('exige tipo de pase', () => {
    expect(validarSolicitud(solicitud({ tipo_pase: null }), AHORA)).toBe(
      'Debe seleccionar un tipo de pase',
    );
  });

  it('exige una edad por visitante', () => {
    expect(validarSolicitud(solicitud({ edades: [30] }), AHORA)).toBe(
      'Debe indicar la edad de cada visitante',
    );
  });

  it('rechaza edades fuera de rango', () => {
    expect(validarSolicitud(solicitud({ edades: [30, 121] }), AHORA)).toBe(
      'Las edades deben estar entre 0 y 120',
    );
  });

  it('rechaza fechas pasadas', () => {
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-10-21' }), AHORA)).toBe(
      'La fecha de visita debe ser hoy o una fecha futura',
    );
  });

  it('rechaza más de un mes de anticipación', () => {
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-11-23' }), AHORA)).toBe(
      'Solo se pueden comprar entradas con hasta 1 mes de anticipación',
    );
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-11-22' }), AHORA)).toBeNull();
  });

  it('rechaza compras para hoy después de las 17:30', () => {
    const tarde = new Date(2026, 9, 22, 17, 31);
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-10-22' }), tarde)).toBe(
      'Las compras para el día de hoy se permiten hasta las 17:30',
    );
    const justo = new Date(2026, 9, 22, 17, 30);
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-10-22' }), justo)).toBeNull();
  });

  it('rechaza lunes y feriados', () => {
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-10-26' }), AHORA)).toBe(
      'El parque está cerrado en la fecha seleccionada',
    );
    const diciembre = new Date(2026, 11, 20, 10, 0);
    expect(validarSolicitud(solicitud({ fecha_visita: '2026-12-25' }), diciembre)).toBe(
      'El parque está cerrado en la fecha seleccionada',
    );
  });

  it('rechaza emails inválidos', () => {
    expect(validarSolicitud(solicitud({ usuario_email: 'ana' }), AHORA)).toBe(
      'Ingresá un email válido',
    );
  });
});

describe('calendario', () => {
  it('suma un mes respetando el fin de mes', () => {
    expect(sumarUnMes({ anio: 2026, mes: 1, dia: 31 })).toEqual({ anio: 2026, mes: 2, dia: 28 });
    expect(sumarUnMes({ anio: 2026, mes: 12, dia: 15 })).toEqual({ anio: 2027, mes: 1, dia: 15 });
  });

  it('calcula el rango permitido', () => {
    expect(rangoFechasPermitidas(AHORA)).toEqual({ min: '2026-10-22', max: '2026-11-22' });
  });

  it('deshabilita lunes y hoy después de hora', () => {
    expect(fechaSeleccionable('2026-10-26', AHORA)).toBe(false);
    expect(fechaSeleccionable('2026-10-27', AHORA)).toBe(true);
    expect(fechaSeleccionable('2026-10-22', new Date(2026, 9, 22, 18, 0))).toBe(false);
  });
});

describe('cálculo de precios según FAQ del PO', () => {
  it('calcula entradas regulares con descuento por edad', () => {
    expect(calcularPrecioEntrada('REGULAR', 3)).toBe(0);
    expect(calcularPrecioEntrada('REGULAR', 15)).toBe(5000);
    expect(calcularPrecioEntrada('REGULAR', 16)).toBe(10000);
    expect(calcularPrecioEntrada('REGULAR', 59)).toBe(10000);
    expect(calcularPrecioEntrada('REGULAR', 60)).toBe(5000);
  });

  it('calcula entradas VIP con el precio base y descuentos del PO', () => {
    expect(calcularPrecioEntrada('VIP', 3)).toBe(0);
    expect(calcularPrecioEntrada('VIP', 4)).toBe(10000);
    expect(calcularPrecioEntrada('VIP', 60)).toBe(10000);
    expect(calcularTotalEntradas('VIP', [3, 10, 30, 60])).toBe(40000);
  });
});

describe('límite acumulado de entradas por usuario y fecha', () => {
  it('permite compras que no superan las 10 entradas acumuladas', () => {
    expect(validarLimiteAcumuladoEntradas(0, 10)).toBeNull();
    expect(validarLimiteAcumuladoEntradas(6, 4)).toBeNull();
  });

  it('rechaza una compra que supera las 10 entradas acumuladas', () => {
    expect(validarLimiteAcumuladoEntradas(8, 3)).toBe(
      'Solo podés comprar hasta 10 entradas para una misma fecha',
    );
  });
});

describe('soloDigitosEdad', () => {
  it('deja pasar números', () => {
    expect(soloDigitosEdad('30')).toBe('30');
  });

  it('descarta letras y otros símbolos', () => {
    expect(soloDigitosEdad('abc')).toBe('');
    expect(soloDigitosEdad('2a5')).toBe('25');
    expect(soloDigitosEdad('-5')).toBe('5');
    expect(soloDigitosEdad('1e2')).toBe('12');
    expect(soloDigitosEdad(' 4 0 ')).toBe('40');
  });

  it('admite como máximo 3 dígitos (edad máxima 120)', () => {
    expect(soloDigitosEdad('1234')).toBe('123');
  });
});
