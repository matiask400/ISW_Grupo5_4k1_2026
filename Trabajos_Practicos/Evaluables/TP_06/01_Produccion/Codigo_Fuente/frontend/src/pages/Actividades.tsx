import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonPage,
} from '@ionic/react';
import { leafOutline } from 'ionicons/icons';
import Encabezado from '../components/Encabezado';
import { actividades } from '../data/actividades';

const Actividades: React.FC = () => (
  <IonPage>
    <Encabezado titulo="Actividades" />
    <IonContent className="con-fondo">
      <div className="contenedor">
        <IonCard>
          <IonCardHeader>
            <IonCardSubtitle><IonIcon icon={leafOutline} /> Viví el parque</IonCardSubtitle>
            <IonCardTitle>Actividades para conectar con la naturaleza</IonCardTitle>
          </IonCardHeader>
          <div className="actividades-intro">
            <p>Explorá las propuestas, elegí tu favorita y preparate para disfrutar al aire libre.</p>
          </div>
          <IonCardContent className="ion-no-padding">
            <IonList lines="none">
              {actividades.map((actividad) => (
                <IonItem key={actividad.nombre} className="actividad-item">
                  <IonIcon slot="start" icon={actividad.icono} color="primary" />
                  <IonLabel>
                    <h2>{actividad.nombre}</h2>
                    <p>{actividad.descripcion}</p>
                  </IonLabel>
                </IonItem>
              ))}
            </IonList>
          </IonCardContent>
        </IonCard>
      </div>
    </IonContent>
  </IonPage>
);

export default Actividades;
