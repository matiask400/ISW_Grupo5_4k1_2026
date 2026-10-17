
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


export function validarNumeroTarjeta(numero: string): boolean {
  const normalizado = numero.replace(/[\s-]/g, '');

  // Solo dígitos y una longitud habitual de tarjeta.
  if (!/^\d{13,19}$/.test(normalizado)) {
    return false;
  }

  let suma = 0;
  let duplicar = false;

  for (let i = normalizado.length - 1; i >= 0; i--) {
    let digito = Number(normalizado[i]);

    if (duplicar) {
      digito *= 2;

      if (digito > 9) {
        digito -= 9;
      }
    }

    suma += digito;
    duplicar = !duplicar;
  }

  return suma % 10 === 0;
}


export function validarCVV(
  cvv: string,
  marca: MarcaTarjeta
): boolean {
  if (marca === 'VISA' || marca === 'MASTERCARD') {
    return /^\d{3}$/.test(cvv);
  }

  if (marca === 'AMEX') {
    return /^\d{4}$/.test(cvv);
  }

  return false;
}
