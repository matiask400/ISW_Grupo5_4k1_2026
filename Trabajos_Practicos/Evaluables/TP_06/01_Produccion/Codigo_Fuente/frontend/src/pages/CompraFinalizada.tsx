import {
  IonButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonContent,
  IonIcon,
  IonPage,
} from '@ionic/react';
import { alertCircleOutline, checkmarkCircleOutline, mailOutline, timeOutline } from 'ionicons/icons';
import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import Encabezado from '../components/Encabezado';
import { leerUltimaCompra } from '../services/ultimaCompra';

/** Estados con los que Mercado Pago vuelve a la back_url (?status=...). */
const ESTADOS_PAGO = {
  approved: { titulo: 'Pago aprobado', icono: checkmarkCircleOutline, color: 'primary' },
  pending: { titulo: 'Pago pendiente', icono: timeOutline, color: 'warning' },
  rejected: { titulo: 'Pago rechazado', icono: alertCircleOutline, color: 'danger' },
} as const;

const PAGO_NO_COMPLETADO = { titulo: 'Pago no completado', icono: alertCircleOutline, color: 'danger' };

/**
 * Página de retorno de Mercado Pago (URL_RETORNO_PAGO en backend/.env).
 * Muestra el estado del pago y la compra registrada (cantidad, fecha y mail).
 */
const CompraFinalizada: React.FC = () => {
  const { search } = useLocation();
  const parametros = new URLSearchParams(search);
  const status = parametros.get('status') ?? parametros.get('collection_status') ?? '';
  const estado = ESTADOS_PAGO[status as keyof typeof ESTADOS_PAGO] ?? PAGO_NO_COMPLETADO;
  const compra = useMemo(() => leerUltimaCompra(), []);

  return (
    <IonPage>
      <Encabezado titulo="Compra finalizada" />
      <IonContent className="con-fondo">
        <div className="contenedor">
          <IonCard className="pago-exitoso-card">
            <IonCardHeader>
              <IonCardSubtitle>Mercado Pago</IonCardSubtitle>
              <IonCardTitle>{estado.titulo}</IonCardTitle>
            </IonCardHeader>
            <IonCardContent className="ion-text-center">
              <IonIcon icon={estado.icono} className="icono-grande" color={estado.color} />
              {status === 'pending' && <p>Mercado Pago te va a avisar cuando se acredite el pago.</p>}
              {(status === 'rejected' || !(status in ESTADOS_PAGO)) && (
                <p>El pago no se completó. Podés intentar de nuevo o pagar en efectivo en boletería.</p>
              )}
              {/* Cantidad de entradas y fecha (CA8) */}
              {compra?.mensaje && <p>{compra.mensaje}</p>}
              {compra?.mail_enviado_a && (
                <p>
                  <IonIcon icon={mailOutline} /> Te enviamos la confirmación a{' '}
                  <strong>{compra.mail_enviado_a}</strong>
                </p>
              )}
              <IonButton routerLink="/inicio" routerDirection="root">
                Volver al inicio
              </IonButton>
            </IonCardContent>
          </IonCard>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default CompraFinalizada;
