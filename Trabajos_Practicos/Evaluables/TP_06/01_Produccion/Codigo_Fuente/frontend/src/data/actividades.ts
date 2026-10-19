import { bicycleOutline, flowerOutline, pawOutline, trailSignOutline } from 'ionicons/icons';

export interface Actividad {
  nombre: string;
  descripcion: string;
  icono: string;
}

export const actividades: Actividad[] = [
  {
    nombre: 'Senderismo',
    descripcion: 'Recorridos guiados por los senderos del parque.',
    icono: trailSignOutline,
  },
  {
    nombre: 'Avistaje de fauna',
    descripcion: 'Conocé los animales que habitan la reserva.',
    icono: pawOutline,
  },
  {
    nombre: 'Jardín botánico',
    descripcion: 'Flora nativa y talleres de jardinería.',
    icono: flowerOutline,
  },
  {
    nombre: 'Bicicleteada',
    descripcion: 'Circuitos para recorrer el parque en bici.',
    icono: bicycleOutline,
  },
];
