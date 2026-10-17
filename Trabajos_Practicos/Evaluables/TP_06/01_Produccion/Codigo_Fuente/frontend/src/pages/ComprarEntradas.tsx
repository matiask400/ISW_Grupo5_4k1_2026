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
  IonModal,
  IonPage,
  IonRadio,
  IonRadioGroup,
  IonSpinner,
  IonText,
} from '@ionic/react';
import { addOutline, removeOutline } from 'ionicons/icons';
import { useMemo, useState } from 'react';
import CorreoSimulado from '../components/CorreoSimulado';
import Encabezado from '../components/Encabezado';
import { useOnline } from '../hooks/useOnline';
import { comprarEntradas } from '../services/api';
import {
  EDAD_MAXIMA,
  EDAD_MINIMA,
  MAXIMO_ENTRADAS_POR_COMPRA,
  MINIMO_ENTRADAS_POR_COMPRA,
  calcularPrecioEntrada,
  calcularTotalEntradas,
  fechaSeleccionable,
  rangoFechasPermitidas,
  validarSolicitud,
} from '../services/reglasCompra';
import type { FormaPago, ResultadoCompra, SolicitudCompra, TipoPase } from '../services/tipos';
import { guardarUltimaCompra } from '../services/ultimaCompra';
import MercadoPagoFormulario from '../components/MercadoPagoFormulario';

/** Único usuario registrado en el backend (USUARIO_DEMO en api/dependencias.py). */
const USUARIO_DEMO = 'prueba@gmail.com';

const ComprarEntradas: React.FC = () => {
  const online = useOnline();

  // Sesión simulada (FAQ 19): arranca con el usuario registrado de prueba.
  const [email, setEmail] = useState(USUARIO_DEMO);
  const [fecha, setFecha] = useState<string | undefined>(undefined);
  const [edades, setEdades] = useState<string[]>(['']); // una por visitante
  const [tipoPase, setTipoPase] = useState<TipoPase | null>(null);
  const [formaPago, setFormaPago] = useState<FormaPago | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [correoCompra, setCorreoCompra] = useState<ResultadoCompra | null>(null);

  const cantidad = edades.length;
  const edadesCompletas = edades.every(
    (edad) => edad.trim() !== '' && Number.isInteger(Number(edad)) && Number(edad) >= EDAD_MINIMA && Number(edad) <= EDAD_MAXIMA,
  );
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
      guardarUltimaCompra(resultado);
      // Con tarjeta el backend devuelve el link de Mercado Pago para pagar (FAQ 4).
      if (resultado.url_pago) {
        window.location.assign(resultado.url_pago);
        return;
      }
      limpiarFormulario();
      // Se representa el correo y su adjunto en pantalla; no se envía un email real.
      setCorreoCompra(resultado);
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
                    label="Usuario (email)"
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
              <IonNote className="ion-padding-horizontal nota">
                Sesión simulada: solo pueden comprar usuarios registrados ({USUARIO_DEMO}). Cambiá el
                email para probar con un usuario no registrado.
              </IonNote>

              {/* Fecha de visita */}
              <IonListHeader>
                <IonLabel>Fecha de visita</IonLabel>
              </IonListHeader>
              <IonNote className="ion-padding-horizontal nota">
                El parque abre de 8:30 a 19 y cierra los lunes, el 25/12 y el 1/1. Para hoy se puede
                comprar hasta las 17:30, y hasta con 1 mes de anticipación.
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
              <IonNote className="ion-padding-horizontal nota">
                Hasta 3 años no pagan. Hasta 15 años y desde 60 años tienen 50% de descuento.
              </IonNote>
              <IonList>
                <IonRadioGroup
                  value={tipoPase}
                  onIonChange={(e) => setTipoPase(e.detail.value as TipoPase)}
                >
                  <IonItem>
                    <IonRadio value="REGULAR" justify="space-between">
                      Regular — $10.000
                    </IonRadio>
                  </IonItem>
                  <IonItem>
                    <IonRadio value="VIP" justify="space-between">
                      VIP — $20.000
                    </IonRadio>
                  </IonItem>
                </IonRadioGroup>
              </IonList>

              {/* Resumen de precio actualizado según las edades ingresadas */}
              {tipoPase && (
                <IonCard className="resumen-precio">
                  <IonCardHeader><IonCardTitle>Resumen de compra</IonCardTitle></IonCardHeader>
                  <IonCardContent>
                    {edades.map((edad, i) => (
                      <p key={i}>Visitante {i + 1}: {edad.trim() === '' ? 'Ingresá una edad' : new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 }).format(calcularPrecioEntrada(tipoPase, Number(edad)))}</p>
                    ))}
                    {edadesCompletas ? (
                      <p><strong>Total estimado: {new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 }).format(calcularTotalEntradas(tipoPase, edades.map(Number)))}</strong></p>
                    ) : (
                      <p className="nota">Completá una edad válida para cada visitante para calcular el total.</p>
                    )}
                  </IonCardContent>
                </IonCard>
              )}

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
                      Efectivo (en boletería)
                    </IonRadio>
                  </IonItem>
                  <IonItem>
                    <IonRadio value="TARJETA" justify="space-between">
                      Tarjeta de crédito (Mercado Pago)
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

                {formaPago === 'TARJETA' && tipoPase && edadesCompletas ? (
                  <MercadoPagoFormulario
                    monto={calcularTotalEntradas(tipoPase, edades.map(Number))}
                    procesando={enviando}
                    onConfirmar={comprar}
                  />
                ) : (
                  <IonButton
                    expand="block"
                    onClick={comprar}
                    disabled={enviando || !online}
                  >
                    {enviando ? <IonSpinner name="crescent" /> : 'Comprar'}
                  </IonButton>
                )}
              </div>

            </IonCardContent>
          </IonCard>
        </div>
      </IonContent>
      <IonModal isOpen={correoCompra !== null} onDidDismiss={() => setCorreoCompra(null)}>
        {correoCompra && (
          <div className="contenedor correo-modal">
            <CorreoSimulado compra={correoCompra} onCerrar={() => setCorreoCompra(null)} />
          </div>
        )}
      </IonModal>
    </IonPage>
  );
};

export default ComprarEntradas;
