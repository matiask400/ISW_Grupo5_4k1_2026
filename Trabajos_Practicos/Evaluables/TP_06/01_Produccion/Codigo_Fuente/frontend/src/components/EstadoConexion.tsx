import { IonBadge } from '@ionic/react';
import { useOnline } from '../hooks/useOnline';


const EstadoConexion: React.FC = () => {
  const online = useOnline();
  return (
    <IonBadge className="badge-conexion" color={online ? 'green' : 'danger'}>
      {online ? 'En línea' : 'Sin conexión'}
    </IonBadge>
  );
};

export default EstadoConexion;
