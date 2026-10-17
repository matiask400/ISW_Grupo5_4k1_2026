import {
  IonButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonIcon,
  IonItem,
  IonLabel,
} from '@ionic/react';
import { attachOutline, checkmarkCircleOutline, mailOutline } from 'ionicons/icons';
import type { ResultadoCompra } from '../services/tipos';

interface Props {
  compra: ResultadoCompra;
  onCerrar?: () => void;
}

/** Representación visual del correo de confirmación; no envía un email real. */
const CorreoSimulado: React.FC<Props> = ({ compra, onCerrar }) => (
  <IonCard className="correo-simulado">
    <IonCardHeader>
      <IonCardSubtitle><IonIcon icon={mailOutline} /> Bandeja de entrada · Simulación</IonCardSubtitle>
      <IonCardTitle>Tu compra en Eco Harmony Park</IonCardTitle>
    </IonCardHeader>
    <IonCardContent>
      <p><strong>De:</strong> Eco Harmony Park &lt;entradas@ecoharmonypark.test&gt;</p>
      <p><strong>Para:</strong> {compra.mail_enviado_a}</p>
      <p><strong>Asunto:</strong> Confirmación de compra {compra.numero_orden ? `· ${compra.numero_orden}` : ''}</p>
      <hr />
      <p>¡Gracias por tu compra! Tu operación fue registrada correctamente.</p>
      {compra.numero_orden && <p><strong>Número de orden:</strong> {compra.numero_orden}</p>}
      {compra.fecha_visita && <p><strong>Fecha de visita:</strong> {compra.fecha_visita}</p>}
      {compra.detalle_visitantes?.map((visitante, index) => (
        <p key={`${visitante.edad}-${index}`}>Visitante {index + 1} · {visitante.edad} años: <strong>{new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 }).format(visitante.subtotal)}</strong></p>
      ))}
      <p><strong>Total: {new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 }).format(compra.monto_total ?? 0)}</strong></p>
      <IonItem lines="none" className="adjunto-simulado">
        <IonIcon slot="start" icon={attachOutline} />
        <IonLabel>
          <h3>{compra.adjunto_nombre ?? 'Entradas_EcoHarmony.pdf'}</h3>
          <p>Archivo adjunto simulado · PDF</p>
        </IonLabel>
        <IonIcon slot="end" icon={checkmarkCircleOutline} color="success" />
      </IonItem>
      {onCerrar && <IonButton expand="block" onClick={onCerrar}>Continuar</IonButton>}
    </IonCardContent>
  </IonCard>
);

export default CorreoSimulado;