
import { describe, expect, it } from 'vitest';
import { detectarMarcaTarjeta } from './tarjetas';

describe('detectarMarcaTarjeta', () => {
  it('detecta Visa cuando el número comienza con 4', () => {
    expect(detectarMarcaTarjeta('4111111111111111')).toBe('VISA');
  });

  it('detecta Mastercard cuando comienza con 51', () => {
    expect(detectarMarcaTarjeta('5111111111111118')).toBe('MASTERCARD');
  });

  it('detecta American Express cuando comienza con 34', () => {
    expect(detectarMarcaTarjeta('341111111111111')).toBe('AMEX');
  });

  it('detecta American Express cuando comienza con 37', () => {
    expect(detectarMarcaTarjeta('371111111111111')).toBe('AMEX');
  });

  it('ignora los espacios del número', () => {
    expect(detectarMarcaTarjeta('4111 1111 1111 1111')).toBe('VISA');
  });

  it('devuelve DESCONOCIDA si no reconoce la marca', () => {
    expect(detectarMarcaTarjeta('6011111111111117')).toBe('DESCONOCIDA');
  });

  it('devuelve DESCONOCIDA si el campo está vacío', () => {
    expect(detectarMarcaTarjeta('')).toBe('DESCONOCIDA');
  });
  it('ignora guiones y otros caracteres que no son dígitos', () => {
  expect(detectarMarcaTarjeta('4111-1111-1111-1111')).toBe('VISA');
});
});
