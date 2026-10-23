import { IonButtons, IonHeader, IonMenuButton, IonTitle, IonToolbar } from '@ionic/react';
import EstadoConexion from './EstadoConexion';

interface Props {
  titulo: string;
}

const Encabezado: React.FC<Props> = ({ titulo }) => (
  <IonHeader>
    <IonToolbar>
      <IonButtons slot="start">
        <IonMenuButton aria-label="Abrir menú" />
      </IonButtons>
      <img src="/icons/icon-192.png" alt="" className="logo-encabezado" slot="start" />
      <IonTitle>{titulo}</IonTitle>
      <div slot="end" className="ion-padding-end">
        <EstadoConexion />
      </div>
    </IonToolbar>
  </IonHeader>
);

export default Encabezado;
