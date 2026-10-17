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
import { checkmarkCircleOutline, mailOutline } from 'ionicons/icons';
import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import Encabezado from '../components/Encabezado';
import { leerUltimaCompra } from '../services/ultimaCompra';

/**
 * Simula Mercado Pago (FAQ 4). El backend redirige acá (PasarelaMercadoPagoSimulada)
 * con el monto a pagar: ?monto=20000
 */
const MercadoPagoSimulado: React.FC = () => {
  const { search } = useLocation();
  const monto = Number(new URLSearchParams(search).get('monto') ?? 0);
  const compra = useMemo(() => leerUltimaCompra(), []);

  return (
    <IonPage>
      <Encabezado titulo="Mercado Pago" />
      <IonContent className="con-fondo">
        <div className="contenedor">
          <IonCard>
            <IonCardHeader>
              <IonCardSubtitle>Mercado Pago (simulado)</IonCardSubtitle>
              <IonCardTitle>Compra exitosa</IonCardTitle>
            </IonCardHeader>
            <IonCardContent className="ion-text-center">
              <IonIcon icon={checkmarkCircleOutline} className="icono-grande" color="primary" />
              <p>
                Pagaste <strong>${monto.toLocaleString('es-AR')}</strong> con tarjeta de crédito.
              </p>
              {/* Cantidad de entradas y fecha (CA8) */}
              {compra?.mensaje && <p>{compra.mensaje}</p>}
              {/* Mail de confirmación (FAQ 5) */}
              {compra?.mail_enviado_a && (
                <p>
                  <IonIcon icon={mailOutline} /> Mail enviado a <strong>{compra.mail_enviado_a}</strong>
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

export default MercadoPagoSimulado;
