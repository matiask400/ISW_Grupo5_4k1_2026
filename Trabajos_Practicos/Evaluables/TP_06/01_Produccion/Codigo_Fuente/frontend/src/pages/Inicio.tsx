import {
  IonButton,
  IonCard,
  IonCardContent,
  IonContent,
  IonIcon,
  IonPage,
} from '@ionic/react';
import { downloadOutline, leafOutline, mapOutline, pawOutline, ticketOutline, timeOutline } from 'ionicons/icons';
import Encabezado from '../components/Encabezado';
import { useInstalarApp } from '../hooks/useInstalarApp';

const Inicio: React.FC = () => {
  const { puedeInstalar, instalar } = useInstalarApp();

  return (
    <IonPage>
      <Encabezado titulo="EcoHarmony Park" />
      <IonContent className="con-fondo">
        <div className="contenedor inicio-contenedor">
          <section className="hero-inicio" aria-labelledby="titulo-inicio">
            <div className="hero-contenido">
              <span className="hero-eyebrow"><IonIcon icon={leafOutline} /> Naturaleza · aventura · bienestar</span>
              <h1 id="titulo-inicio">Respirá naturaleza.</h1>
              <p>Un lugar para descubrir, explorar y conectar con lo mejor del mundo natural.</p>
              <div className="hero-acciones">
                <IonButton routerLink="/entradas" routerDirection="root" color="tertiary">
                  <IonIcon slot="start" icon={ticketOutline} /> Comprar entradas
                </IonButton>
                <IonButton routerLink="/actividades" routerDirection="root" fill="outline" color="light">
                  Explorar actividades
                </IonButton>
              </div>
            </div>
          </section>

          <section className="tarjetas-beneficio" aria-label="Información del parque">
            <div className="beneficio">
              <IonIcon icon={pawOutline} />
              <strong>Encuentros naturales</strong>
              <span>Descubrí la fauna y la flora del parque.</span>
            </div>
            <div className="beneficio">
              <IonIcon icon={timeOutline} />
              <strong>Planificá tu visita</strong>
              <span>Elegí una fecha y prepará tu recorrido.</span>
            </div>
            <div className="beneficio">
              <IonIcon icon={mapOutline} />
              <strong>Todo a mano</strong>
              <span>Consultá las actividades y el mapa del parque.</span>
            </div>
          </section>

          <IonCard className="inicio-panel">
            <IonCardContent>
              <h2>Tu próxima aventura empieza acá</h2>
              <p>Comprá tus entradas, conocé las actividades disponibles y organizá una experiencia a tu ritmo.</p>
              <div className="accesos">
                <IonButton routerLink="/entradas" routerDirection="root">
                  <IonIcon slot="start" icon={ticketOutline} /> Comprar entradas
                </IonButton>
                <IonButton routerLink="/actividades" routerDirection="root" fill="outline">
                  <IonIcon slot="start" icon={leafOutline} /> Actividades
                </IonButton>
                <IonButton routerLink="/mapa" routerDirection="root" fill="outline">
                  <IonIcon slot="start" icon={mapOutline} /> Mapa
                </IonButton>
              </div>
            </IonCardContent>
          </IonCard>

          {puedeInstalar && (
            <IonCard>
              <IonCardContent>
                <h2>EcoHarmony, siempre cerca</h2>
                <p>Instalá la app en tu dispositivo para tenerla siempre a mano.</p>
                <IonButton expand="block" color="secondary" onClick={instalar}>
                  <IonIcon slot="start" icon={downloadOutline} /> Instalar app
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
