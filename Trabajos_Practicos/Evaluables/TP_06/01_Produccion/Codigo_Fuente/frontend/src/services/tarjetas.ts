
export type MarcaTarjeta =
  | 'VISA'
  | 'MASTERCARD'
  | 'AMEX'
  | 'DESCONOCIDA';

export function detectarMarcaTarjeta(numero: string): MarcaTarjeta {
  const digitos = numero.replace(/\D/g, '');

  if (digitos.startsWith('4')) {
    return 'VISA';
  }

  if (/^5[1-5]/.test(digitos)) {
    return 'MASTERCARD';
  }

  if (/^3[47]/.test(digitos)) {
    return 'AMEX';
  }

  return 'DESCONOCIDA';
}
