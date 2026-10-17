
import { describe, expect, it } from 'vitest';
import { detectarMarcaTarjeta } from './tarjetas';
import { validarNumeroTarjeta } from './tarjetas';


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


describe('validarNumeroTarjeta', () => {
  it('acepta un número Visa de prueba válido', () => {
    expect(validarNumeroTarjeta('4111111111111111')).toBe(true);
  });

  it('acepta espacios entre los dígitos', () => {
    expect(validarNumeroTarjeta('4111 1111 1111 1111')).toBe(true);
  });

  it('rechaza un número que no supera Luhn', () => {
    expect(validarNumeroTarjeta('4111111111111112')).toBe(false);
  });

  it('rechaza un número demasiado corto', () => {
    expect(validarNumeroTarjeta('411111')).toBe(false);
  });

  it('rechaza un campo vacío', () => {
    expect(validarNumeroTarjeta('')).toBe(false);
  });

  it('rechaza letras', () => {
    expect(validarNumeroTarjeta('abcd')).toBe(false);
  });

  it('rechaza una longitud no admitida', () => {
    expect(validarNumeroTarjeta('41111111111111111111')).toBe(false);
  });
  it('acepta guiones entre los dígitos', () => {
  expect(validarNumeroTarjeta('4111-1111-1111-1111')).toBe(true);
});

it('rechaza símbolos distintos de espacios y guiones', () => {
  expect(validarNumeroTarjeta('4111/1111/1111/1111')).toBe(false);
});
});

