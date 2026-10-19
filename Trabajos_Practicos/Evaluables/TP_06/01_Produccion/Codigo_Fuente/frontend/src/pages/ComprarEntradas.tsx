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
  useIonAlert,
  useIonRouter,
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
  calcularPrecioEntrada,
  calcularTotalEntradas,
  fechaSeleccionable,
  rangoFechasPermitidas,
  soloDigitosEdad,
  validarSolicitud,
} from '../services/reglasCompra';
import type { FormaPago, SolicitudCompra, TipoPase } from '../services/tipos';
import { guardarUltimaCompra } from '../services/ultimaCompra';

/** Único usuario registrado en el backend (USUARIO_DEMO en api/dependencias.py). */
const USUARIO_DEMO = 'tinchoimo@gmail.com';

const ComprarEntradas: React.FC = () => {
  const online = useOnline();
  const [mostrarAlerta] = useIonAlert();
  const router = useIonRouter();

  // Sesión simulada (FAQ 19): arranca con el usuario registrado de prueba.
  const [email, setEmail] = useState(USUARIO_DEMO);
  const [fecha, setFecha] = useState<string | undefined>(undefined);
  const [edades, setEdades] = useState<string[]>(['']); // una por visitante
  const [tipoPase, setTipoPase] = useState<TipoPase | null>(null);
  const [formaPago, setFormaPago] = useState<FormaPago | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const [pasoActivo, setPasoActivo] = useState(1);
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
    setPasoActivo(1);
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
    setPasoActivo(3);
    setEnviando(true);
    const resultado = await comprarEntradas(solicitud);
    setEnviando(false);

    if (resultado.exitosa) {
      setPasoActivo(4);
      guardarUltimaCompra(solicitud.usuario_email, resultado);
      // Con tarjeta el backend devuelve el checkout de Mercado Pago; al terminar,
      // Mercado Pago vuelve a /compra-finalizada.
      if (resultado.url_pago) {
        window.location.assign(resultado.url_pago);
        return;
      }
      limpiarFormulario();
      // En efectivo: se informa cantidad, fecha y total (CA8) y a dónde se mandó el mail.
      await mostrarAlerta({
        header: '¡Compra realizada!',
        subHeader: `Te enviamos la confirmación a ${resultado.mail_enviado_a}`,
        message: `${resultado.mensaje ?? ''}. Pagás en boletería al llegar al parque.`,
        buttons: ['Aceptar'],
        // Al cerrar el aviso (con "Aceptar" o tocando afuera) se vuelve al inicio.
        onDidDismiss: () => router.push('/inicio', 'root', 'replace'),
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
          <div className="compra-intro"><span className="sobrelinea">TU VISITA, A TU MANERA</span><h1>Prepará tu experiencia.</h1><p>Completá los pasos y revisá el resumen antes de confirmar.</p></div>
          <div className="pasos-compra" aria-label="Pasos de compra">{[{n:1,t:'Fecha'},{n:2,t:'Entradas'},{n:3,t:'Pago'},{n:4,t:'Confirmación'}].map((p) => <button type="button" key={p.n} className={`paso-compra ${pasoActivo === p.n ? 'activo' : ''} ${pasoActivo > p.n ? 'completado' : ''}`} onClick={() => { setPasoActivo(p.n); document.getElementById(p.n === 1 ? 'paso-fecha' : p.n === 2 ? 'paso-entradas' : p.n === 3 ? 'paso-pago' : 'resumen-compra')?.scrollIntoView({behavior:'smooth',block:'start'}); }}><span>{pasoActivo > p.n ? '✓' : p.n}</span><strong>{p.t}</strong></button>)}</div>
          <div className="compra-layout"><div className="compra-formulario"><IonCard className="compra-card">
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
              <div id="paso-fecha" className="ancla-compra"><IonListHeader>
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
              </div></div>

              {/* Cantidad y edades */}
              <div id="paso-entradas" className="ancla-compra"><IonListHeader>
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
                      type="text"
                      inputmode="numeric"
                      pattern="[0-9]*"
                      maxlength={String(EDAD_MAXIMA).length}
                      placeholder="Ej: 30"
                      value={edad}
                      onIonInput={(e) => {
                        // Solo números: se borra lo que no sea dígito apenas se escribe.
                        const limpio = soloDigitosEdad(e.detail.value ?? '');
                        e.target.value = limpio;
                        cambiarEdad(i, limpio);
                      }}
                    />
                  </IonItem>
                ))}
              </IonList>

              </div>

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
              <div id="paso-pago" className="ancla-compra"><IonListHeader>
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
              </IonList></div>

              
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
                  {enviando ? (
                    <IonSpinner name="crescent" />
                  ) : formaPago === 'TARJETA' ? (
                    'Pagar con Mercado Pago'
                  ) : (
                    'Comprar'
                  )}
                </IonButton>
              </div>

            </IonCardContent>
          </IonCard></div><aside className="compra-resumen-lateral" id="resumen-compra"><span className="sobrelinea">TU RESUMEN</span><h2>Tu visita</h2><div className="resumen-lateral-linea"><span>Fecha</span><strong>{fecha ? new Intl.DateTimeFormat('es-AR',{dateStyle:'medium'}).format(new Date(`${fecha.slice(0,10)}T12:00:00`)) : 'A elegir'}</strong></div><div className="resumen-lateral-linea"><span>Visitantes</span><strong>{cantidad} {cantidad === 1 ? 'persona' : 'personas'}</strong></div><div className="resumen-lateral-linea"><span>Tipo de pase</span><strong>{tipoPase === 'VIP' ? 'VIP' : tipoPase === 'REGULAR' ? 'Regular' : 'A elegir'}</strong></div><div className="resumen-lateral-linea"><span>Forma de pago</span><strong>{formaPago === 'TARJETA' ? 'Tarjeta' : formaPago === 'EFECTIVO' ? 'Efectivo' : 'A elegir'}</strong></div><div className="resumen-lateral-total"><span>Total estimado</span><strong>{tipoPase && edadesCompletas ? new Intl.NumberFormat('es-AR',{style:'currency',currency:'ARS',maximumFractionDigits:0}).format(calcularTotalEntradas(tipoPase,edades.map(Number))) : '—'}</strong></div><p>El total se calcula según el tipo de pase y la edad de cada visitante.</p><div className="resumen-descuentos"><strong>Tarifas y descuentos</strong><span>Regular: $10.000</span><span>VIP: $20.000</span><span>Hasta 3 años: gratis</span><span>4 a 15 años: 50%</span><span>Desde 60 años: 50%</span></div><div className="resumen-descuentos"><strong>Descuentos aplicados automáticamente</strong><span>Hasta 3 años: gratis</span><span>4 a 15 años: 50%</span><span>Desde 60 años: 50%</span></div></aside></div>
        </div>
      </IonContent>
    </IonPage>
  );
};

export default ComprarEntradas;
