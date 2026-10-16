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
import { downloadOutline, leafOutline, mapOutline, ticketOutline } from 'ionicons/icons';
import Encabezado from '../components/Encabezado';
import { useInstalarApp } from '../hooks/useInstalarApp';

const Inicio: React.FC = () => {
  const { puedeInstalar, instalar } = useInstalarApp();

  return (
    <IonPage>
      <Encabezado titulo="EcoHarmony Park" />
      <IonContent className="con-fondo">
        <div className="contenedor">
          <IonCard>
            <IonCardHeader>
              <IonCardSubtitle>Bienvenido</IonCardSubtitle>
              <IonCardTitle>EcoHarmony Park</IonCardTitle>
            </IonCardHeader>
            <IonCardContent>
              <p>Seleccioná una opción para continuar.</p>
              <div className="accesos">
                <IonButton routerLink="/entradas" routerDirection="root">
                  <IonIcon slot="start" icon={ticketOutline} />
                  Comprar entradas
                </IonButton>
                <IonButton routerLink="/actividades" routerDirection="root" fill="outline">
                  <IonIcon slot="start" icon={leafOutline} />
                  Actividades
                </IonButton>
                <IonButton routerLink="/mapa" routerDirection="root" fill="outline">
                  <IonIcon slot="start" icon={mapOutline} />
                  Mapa
                </IonButton>
              </div>
            </IonCardContent>
          </IonCard>

          {puedeInstalar && (
            <IonCard>
              <IonCardContent>
                <p>Instalá la app en tu dispositivo para tenerla siempre a mano.</p>
                <IonButton expand="block" color="secondary" onClick={instalar}>
                  <IonIcon slot="start" icon={downloadOutline} />
                  Instalar app
                </IonButton>
              </IonCardContent>
            </IonCard>
          )}
        </div>
      </IonContent>
    </IonPage>
  );
};

export default Inicio;
