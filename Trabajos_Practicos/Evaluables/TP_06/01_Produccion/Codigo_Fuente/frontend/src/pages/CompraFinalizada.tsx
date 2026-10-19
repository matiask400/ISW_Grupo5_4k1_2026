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
  IonSpinner,
} from '@ionic/react';
import { alertCircleOutline, checkmarkCircleOutline, mailOutline, timeOutline } from 'ionicons/icons';
import { useEffect, useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Encabezado from '../components/Encabezado';
import { confirmarPago } from '../services/api';
import type { ResultadoCompra } from '../services/tipos';
import { leerUltimaCompra } from '../services/ultimaCompra';

const CompraFinalizada: React.FC = () => {
  const { search } = useLocation();
  const parametros = new URLSearchParams(search);
  const status = parametros.get('status') ?? parametros.get('collection_status') ?? '';
  const paymentId = parametros.get('payment_id') ?? parametros.get('collection_id');
  const compra = useMemo(() => leerUltimaCompra(), []);

  const [confirmacion, setConfirmacion] = useState<ResultadoCompra | null>(null);
  const aprobado = status === 'approved' && paymentId && compra;

  useEffect(() => {
    if (!aprobado) return;
    confirmarPago(paymentId, compra.usuario_email).then(setConfirmacion);
  }, [aprobado, paymentId, compra]);

  const verificando = aprobado && confirmacion === null;
  const confirmado = confirmacion?.exitosa === true;

  const titulo = verificando
    ? 'Verificando el pago…'
    : confirmado
      ? 'Pago aprobado'
      : status === 'pending'
        ? 'Pago pendiente'
        : 'Pago no completado';

  return (
    <IonPage>
      <Encabezado titulo="Compra finalizada" />
      <IonContent className="con-fondo">
        <div className="contenedor">
          <IonCard className="pago-exitoso-card">
            <IonCardHeader>
              <IonCardSubtitle>Mercado Pago</IonCardSubtitle>
              <IonCardTitle>{titulo}</IonCardTitle>
            </IonCardHeader>
            <IonCardContent className="ion-text-center">
              {verificando ? (
                <IonSpinner name="crescent" />
              ) : confirmado ? (
                <>
                  <IonIcon icon={checkmarkCircleOutline} className="icono-grande" color="primary" />
                  {/* Cantidad de entradas y fecha (CA8) */}
                  <p>{confirmacion.mensaje}</p>
                  {confirmacion.mail_enviado_a && (
                    <p>
                      <IonIcon icon={mailOutline} /> Te enviamos la confirmación a{' '}
                      <strong>{confirmacion.mail_enviado_a}</strong>
                    </p>
                  )}
                </>
              ) : status === 'pending' ? (
                <>
                  <IonIcon icon={timeOutline} className="icono-grande" color="warning" />
                  <p>Mercado Pago todavía no acreditó el pago. Te vamos a avisar cuando se apruebe.</p>
                </>
              ) : (
                <>
                  <IonIcon icon={alertCircleOutline} className="icono-grande" color="danger" />
                  <p>
                    {confirmacion?.error ??
                      'El pago no se completó. Podés intentar de nuevo o pagar en efectivo en boletería.'}
                  </p>
                </>
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
