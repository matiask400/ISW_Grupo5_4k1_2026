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
import { compassOutline, leafOutline, mapOutline } from 'ionicons/icons';
import Encabezado from '../components/Encabezado';

const Mapa: React.FC = () => (
  <IonPage>
    <Encabezado titulo="Mapa del Parque" />
    <IonContent className="con-fondo">
      <div className="contenedor">
        <IonCard>
          <IonCardHeader>
            <IonCardSubtitle><IonIcon icon={compassOutline} /> Explorá a tu ritmo</IonCardSubtitle>
            <IonCardTitle>Mapa del parque</IonCardTitle>
          </IonCardHeader>
          <IonCardContent className="ion-text-center">
            <div className="estado-vacio">
              <IonIcon icon={mapOutline} className="icono-grande" />
              <h2>Estamos preparando el recorrido</h2>
              <p>Próximamente vas a poder consultar el mapa del parque y ubicar sus principales espacios.</p>
              <IonButton routerLink="/actividades" routerDirection="root">
                <IonIcon slot="start" icon={leafOutline} /> Explorar actividades
              </IonButton>
            </div>
          </IonCardContent>
        </IonCard>
      </div>
    </IonContent>
  </IonPage>
);

export default Mapa;
