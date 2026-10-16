import { IonButtons, IonHeader, IonMenuButton, IonTitle, IonToolbar } from '@ionic/react';
import EstadoConexion from './EstadoConexion';

interface Props {
  titulo: string;
}

/** Barra superior común a todas las pantallas (logo, título y menú). */
const Encabezado: React.FC<Props> = ({ titulo }) => (
  <IonHeader>
    <IonToolbar>
      <IonButtons slot="start">
        <IonMenuButton aria-label="Abrir menú" />
      </IonButtons>
      <img src="/icons/icono.jpg" alt="" className="logo-encabezado" slot="start" />
      <IonTitle>{titulo}</IonTitle>
      <div slot="end" className="ion-padding-end">
        <EstadoConexion />
      </div>
    </IonToolbar>
  </IonHeader>
);

export default Encabezado;
