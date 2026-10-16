import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonContent,
  IonIcon,
  IonPage,
} from '@ionic/react';
import { mapOutline } from 'ionicons/icons';
import Encabezado from '../components/Encabezado';

const Mapa: React.FC = () => (
  <IonPage>
    <Encabezado titulo="Mapa del Parque" />
    <IonContent className="con-fondo">
      <div className="contenedor">
        <IonCard>
          <IonCardHeader>
            <IonCardTitle>Mapa del parque</IonCardTitle>
          </IonCardHeader>
          <IonCardContent className="ion-text-center">
            <IonIcon icon={mapOutline} className="icono-grande" color="primary" />
            <p>Próximamente vas a poder ver el mapa del parque acá.</p>
          </IonCardContent>
        </IonCard>
      </div>
    </IonContent>
  </IonPage>
);

export default Mapa;
