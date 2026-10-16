import {
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonPage,
} from '@ionic/react';
import Encabezado from '../components/Encabezado';
import { actividades } from '../data/actividades';

const Actividades: React.FC = () => (
  <IonPage>
    <Encabezado titulo="Actividades" />
    <IonContent className="con-fondo">
      <div className="contenedor">
        <IonCard>
          <IonCardHeader>
            <IonCardTitle>Actividades del parque</IonCardTitle>
          </IonCardHeader>
          <IonCardContent className="ion-no-padding">
            <IonList lines="full">
              {actividades.map((actividad) => (
                <IonItem key={actividad.nombre}>
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
