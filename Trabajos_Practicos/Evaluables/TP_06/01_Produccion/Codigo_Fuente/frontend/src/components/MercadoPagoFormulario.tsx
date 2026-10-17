
import { useState } from 'react';
import {
  IonButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonInput,
  IonItem,
  IonText,
} from '@ionic/react';
import {
  detectarMarcaTarjeta,
  validarDatosTarjeta,
} from '../services/tarjetas';

interface MercadoPagoFormularioProps {
  monto: number;
  onConfirmar: () => void;
  procesando?: boolean;
}

const MercadoPagoFormulario: React.FC<MercadoPagoFormularioProps> = ({
  monto,
  onConfirmar,
  procesando = false,
}) => {
  const [numero, setNumero] = useState('');
  const [cvv, setCvv] = useState('');
  const [error, setError] = useState<string | null>(null);

  const marca = detectarMarcaTarjeta(numero);
  const datosValidos = validarDatosTarjeta(numero, cvv);

  const confirmar = () => {
    if (!datosValidos || procesando) {
      setError('Ingresá un número de tarjeta y CVV válidos.');
      return;
    }

    setError(null);
    onConfirmar();
  };

  const nombreMarca = {
    VISA: 'Visa',
    MASTERCARD: 'Mastercard',
    AMEX: 'American Express',
    DESCONOCIDA: '',
  }[marca];

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>Mercado Pago</IonCardTitle>
      </IonCardHeader>

      <IonCardContent>
        <p>
          Total a pagar:{' '}
          <strong>
            {new Intl.NumberFormat('es-AR', {
              style: 'currency',
              currency: 'ARS',
              maximumFractionDigits: 0,
            }).format(monto)}
          </strong>
        </p>

        <IonItem>
          <IonInput
            label="Número de tarjeta"
            labelPlacement="stacked"
            type="text"
            inputmode="numeric"
            autocomplete="off"
            placeholder="4111 1111 1111 1111"
            value={numero}
            onIonInput={(e) => {
              setNumero(String(e.detail.value ?? '').slice(0, 23));
              setError(null);
            }}
          />
        </IonItem>

        {nombreMarca && (
          <IonText color="primary">
            <p>Tarjeta detectada: {nombreMarca}</p>
          </IonText>
        )}

        <IonItem>
          <IonInput
            label="CVV"
            labelPlacement="stacked"
            type="password"
            inputmode="numeric"
            autocomplete="off"
            placeholder={marca === 'AMEX' ? '4 dígitos' : '3 dígitos'}
            maxlength={marca === 'AMEX' ? 4 : 3}
            value={cvv}
            onIonInput={(e) => {
              const valor = String(e.detail.value ?? '');
              setCvv(valor.replace(/\D/g, '').slice(0, 4));
              setError(null);
            }}
          />
        </IonItem>

        {error && (
          <IonText color="danger" role="alert">
            <p>{error}</p>
          </IonText>
        )}

        <IonButton
          expand="block"
          onClick={confirmar}
          disabled={!datosValidos || procesando}
        >
          {procesando ? 'Procesando...' : 'Pagar'}
        </IonButton>
      </IonCardContent>
    </IonCard>
  );
};

export default MercadoPagoFormulario;
