import {
  IonContent,
  IonHeader,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonMenu,
  IonMenuToggle,
  IonTitle,
  IonToolbar,
} from '@ionic/react';
import { homeOutline, leafOutline, mapOutline, ticketOutline } from 'ionicons/icons';
import { useLocation } from 'react-router-dom';

interface Opcion {
  titulo: string;
  url: string;
  icono: string;
}

const opciones: Opcion[] = [
  { titulo: 'Inicio', url: '/inicio', icono: homeOutline },
  { titulo: 'Actividades', url: '/actividades', icono: leafOutline },
  { titulo: 'Comprar Entradas', url: '/entradas', icono: ticketOutline },
  { titulo: 'Mapa del Parque', url: '/mapa', icono: mapOutline },
];

const Menu: React.FC = () => {
  const location = useLocation();

  return (
    <IonMenu contentId="contenido-principal" type="overlay">
      <IonHeader>
        <IonToolbar>
          <IonTitle>EcoHarmony Park</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonList lines="none">
          {opciones.map((opcion) => (
            <IonMenuToggle key={opcion.url} autoHide={false}>
              <IonItem
                routerLink={opcion.url}
                routerDirection="root"
                className={location.pathname === opcion.url ? 'opcion-seleccionada' : ''}
              >
                <IonIcon aria-hidden="true" slot="start" icon={opcion.icono} />
                <IonLabel>{opcion.titulo}</IonLabel>
              </IonItem>
            </IonMenuToggle>
          ))}
        </IonList>
      </IonContent>
    </IonMenu>
  );
};

export default Menu;
