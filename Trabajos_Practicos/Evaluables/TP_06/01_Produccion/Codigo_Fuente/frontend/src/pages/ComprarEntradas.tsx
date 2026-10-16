import {
  IonButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonContent,
  IonDatetime,
  IonIcon,
  IonInput,
  IonItem,
  IonLabel,
  IonList,
  IonListHeader,
  IonNote,
  IonPage,
  IonRadio,
  IonRadioGroup,
  IonSpinner,
  IonText,
  useIonToast,
} from '@ionic/react';
import { addOutline, removeOutline } from 'ionicons/icons';
import { useMemo, useState } from 'react';
import Encabezado from '../components/Encabezado';
import { useOnline } from '../hooks/useOnline';
import { comprarEntradas } from '../services/api';
import {
  EDAD_MAXIMA,
  EDAD_MINIMA,
  MAXIMO_ENTRADAS_POR_COMPRA,
  MINIMO_ENTRADAS_POR_COMPRA,
  fechaSeleccionable,
  rangoFechasPermitidas,
  validarSolicitud,
} from '../services/reglasCompra';
import type { FormaPago, SolicitudCompra, TipoPase } from '../services/tipos';

const ComprarEntradas: React.FC = () => {
  const online = useOnline();
  const [mostrarToast] = useIonToast();

  const [email, setEmail] = useState('');
  const [fecha, setFecha] = useState<string | undefined>(undefined);
  const [edades, setEdades] = useState<string[]>(['']); // una por visitante
  const [tipoPase, setTipoPase] = useState<TipoPase | null>(null);
  const [formaPago, setFormaPago] = useState<FormaPago | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const cantidad = edades.length;
  const { min, max } = useMemo(() => rangoFechasPermitidas(), []);

  const cambiarCantidad = (nueva: number) => {
    if (nueva < MINIMO_ENTRADAS_POR_COMPRA || nueva > MAXIMO_ENTRADAS_POR_COMPRA) return;
    setEdades((actuales) =>
      nueva > actuales.length
        ? [...actuales, ...Array(nueva - actuales.length).fill('')]
        : actuales.slice(0, nueva),
    );
  };

  const cambiarEdad = (indice: number, valor: string) => {
    setEdades((actuales) => actuales.map((e, i) => (i === indice ? valor : e)));
  };

  const limpiarFormulario = () => {
    setFecha(undefined);
    setEdades(['']);
    setTipoPase(null);
    setFormaPago(null);
    setError(null);
  };

  const comprar = async () => {
    const solicitud: SolicitudCompra = {
      usuario_email: email.trim(),
      fecha_visita: fecha ? fecha.slice(0, 10) : '',
      cantidad,
      edades: edades.map((e) => (e.trim() === '' ? NaN : Number(e))),
      tipo_pase: tipoPase,
      forma_pago: formaPago,
    };

    const errorValidacion = validarSolicitud(solicitud);
    if (errorValidacion) {
      setError(errorValidacion);
      return;
    }

    setError(null);
    setEnviando(true);
    const resultado = await comprarEntradas(solicitud);
    setEnviando(false);

    if (resultado.exitosa) {
      limpiarFormulario();
      await mostrarToast({
        message: '¡Compra realizada con éxito! Te enviamos los detalles por email.',
        duration: 4000,
        color: 'success',
        position: 'top',
      });
    } else {
      setError(resultado.error ?? 'No se pudo completar la compra.');
    }
  };

  return (
    <IonPage>
      <Encabezado titulo="Comprar Entradas" />
      <IonContent className="con-fondo">
        <div className="contenedor">
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>Comprar entradas</IonCardTitle>
            </IonCardHeader>
            <IonCardContent className="ion-no-padding">
              {/* Datos del comprador */}
              <IonList>
                <IonItem>
                  <IonInput
                    label="Email"
                    labelPlacement="stacked"
                    type="email"
                    inputmode="email"
                    autocomplete="email"
                    placeholder="tu@email.com"
                    value={email}
                    onIonInput={(e) => setEmail(e.detail.value ?? '')}
                  />
                </IonItem>
              </IonList>

              {/* Fecha de visita */}
              <IonListHeader>
                <IonLabel>Fecha de visita</IonLabel>
              </IonListHeader>
              <IonNote className="ion-padding-horizontal nota">
                El parque cierra los lunes, el 25/12 y el 1/1. Para hoy se puede comprar hasta las
                17:30.
              </IonNote>
              <div className="calendario">
                <IonDatetime
                  presentation="date"
                  locale="es-AR"
                  firstDayOfWeek={1}
                  min={min}
                  max={max}
                  value={fecha}
                  isDateEnabled={(iso) => fechaSeleccionable(iso)}
                  onIonChange={(e) => {
                    const v = e.detail.value;
                    setFecha(typeof v === 'string' ? v : undefined);
                  }}
                />
              </div>

              {/* Cantidad y edades */}
              <IonListHeader>
                <IonLabel>Visitantes</IonLabel>
              </IonListHeader>
              <IonList>
                <IonItem>
                  <IonLabel>Cantidad de entradas</IonLabel>
                  <div slot="end" className="contador">
                    <IonButton
                      fill="clear"
                      aria-label="Quitar entrada"
                      disabled={cantidad <= MINIMO_ENTRADAS_POR_COMPRA}
                      onClick={() => cambiarCantidad(cantidad - 1)}
                    >
                      <IonIcon slot="icon-only" icon={removeOutline} />
                    </IonButton>
                    <strong>{cantidad}</strong>
                    <IonButton
                      fill="clear"
                      aria-label="Agregar entrada"
                      disabled={cantidad >= MAXIMO_ENTRADAS_POR_COMPRA}
                      onClick={() => cambiarCantidad(cantidad + 1)}
                    >
                      <IonIcon slot="icon-only" icon={addOutline} />
                    </IonButton>
                  </div>
                </IonItem>
                {edades.map((edad, i) => (
                  <IonItem key={i}>
                    <IonInput
                      label={`Edad del visitante ${i + 1}`}
                      labelPlacement="fixed"
                      type="number"
                      inputmode="numeric"
                      min={EDAD_MINIMA}
                      max={EDAD_MAXIMA}
                      placeholder="Ej: 30"
                      value={edad}
                      onIonInput={(e) => cambiarEdad(i, String(e.detail.value ?? ''))}
                    />
                  </IonItem>
                ))}
              </IonList>

              {/* Tipo de pase */}
              <IonListHeader>
                <IonLabel>Tipo de pase</IonLabel>
              </IonListHeader>
              <IonList>
                <IonRadioGroup
                  value={tipoPase}
                  onIonChange={(e) => setTipoPase(e.detail.value as TipoPase)}
                >
                  <IonItem>
                    <IonRadio value="REGULAR" justify="space-between">
                      Regular
                    </IonRadio>
                  </IonItem>
                  <IonItem>
                    <IonRadio value="VIP" justify="space-between">
                      VIP
                    </IonRadio>
                  </IonItem>
                </IonRadioGroup>
              </IonList>

              {/* Forma de pago */}
              <IonListHeader>
                <IonLabel>Forma de pago</IonLabel>
              </IonListHeader>
              <IonList>
                <IonRadioGroup
                  value={formaPago}
                  onIonChange={(e) => setFormaPago(e.detail.value as FormaPago)}
                >
                  <IonItem>
                    <IonRadio value="EFECTIVO" justify="space-between">
                      Efectivo
                    </IonRadio>
                  </IonItem>
                  <IonItem>
                    <IonRadio value="TARJETA" justify="space-between">
                      Tarjeta
                    </IonRadio>
                  </IonItem>
                </IonRadioGroup>
              </IonList>

              <div className="ion-padding">
                {error && (
                  <IonText color="danger" role="alert">
                    <p className="mensaje-error">{error}</p>
                  </IonText>
                )}
                {!online && (
                  <IonText color="medium">
                    <p>Necesitás conexión a internet para comprar.</p>
                  </IonText>
                )}
                <IonButton expand="block" onClick={comprar} disabled={enviando || !online}>
                  {enviando ? <IonSpinner name="crescent" /> : 'Comprar'}
                </IonButton>
              </div>
            </IonCardContent>
          </IonCard>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default ComprarEntradas;
