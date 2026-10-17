import { IonButton, IonCard, IonCardContent, IonContent, IonIcon, IonPage } from '@ionic/react';
import { downloadOutline, leafOutline, mapOutline, pawOutline, ticketOutline, timeOutline, checkmarkCircleOutline, heartOutline, shieldCheckmarkOutline, chevronDownOutline, locationOutline, peopleOutline } from 'ionicons/icons';
import Encabezado from '../components/Encabezado';
import { useInstalarApp } from '../hooks/useInstalarApp';

const preguntas = [
  { q: '¿Cuál es el horario del parque?', a: 'El horario de atención es de 8:30 a 19:00. Te recomendamos llegar con tiempo para disfrutar las actividades.' },
  { q: '¿Qué días está cerrado?', a: 'El parque permanece cerrado los lunes, el 25 de diciembre y el 1 de enero.' },
  { q: '¿Hay entradas con descuento?', a: 'Sí. Los niños de hasta 3 años ingresan gratis. Los visitantes de 4 a 15 años y las personas desde los 60 años tienen un 50% de descuento.' },
  { q: '¿Puedo organizar una visita familiar?', a: '¡Claro! Podés revisar las actividades disponibles y comprar las entradas de todos los visitantes en una misma operación.' },
];

const Inicio: React.FC = () => {
  const { puedeInstalar, instalar } = useInstalarApp();
  return (
    <IonPage>
      <Encabezado titulo="EcoHarmony Park" />
      <IonContent className="con-fondo">
        <div className="contenedor inicio-contenedor inicio-pro">
          <section className="hero-inicio" aria-labelledby="titulo-inicio">
            <div className="hero-contenido hero-entrada">
              <span className="hero-eyebrow"><IonIcon icon={leafOutline} /> Naturaleza · aventura · bienestar</span>
              <h1 id="titulo-inicio">Volvé a conectar<br />con lo esencial.</h1>
              <p>Respirá aire puro, descubrí nuevos paisajes y compartí un día distinto rodeado de naturaleza.</p>
              <div className="hero-acciones">
                <IonButton routerLink="/entradas" routerDirection="root" color="tertiary" size="large"><IonIcon slot="start" icon={ticketOutline} /> Comprar entradas</IonButton>
                <IonButton routerLink="/actividades" routerDirection="root" fill="outline" color="light" size="large">Explorar actividades</IonButton>
              </div>
            </div>
            <a className="hero-scroll" href="#descubri" aria-label="Desplazarse para descubrir el parque"><span>Descubrí el parque</span><IonIcon icon={chevronDownOutline} /></a>
          </section>

          <section id="descubri" className="seccion-inicio intro-parque">
            <div><span className="sobrelinea">TU PRÓXIMA ESCAPADA</span><h2>Un respiro en medio de lo cotidiano.</h2></div>
            <p>Un espacio para bajar el ritmo, explorar al aire libre y crear recuerdos con quienes más querés.</p>
          </section>

          <section className="tarjetas-beneficio beneficios-pro" aria-label="Beneficios de visitar el parque">
            <article className="beneficio"><IonIcon icon={pawOutline} /><strong>Descubrí la naturaleza</strong><span>Conectá con el entorno natural y explorá a tu propio ritmo.</span></article>
            <article className="beneficio"><IonIcon icon={heartOutline} /><strong>Compartí momentos</strong><span>Una experiencia para disfrutar en familia, con amigos o en pareja.</span></article>
            <article className="beneficio"><IonIcon icon={shieldCheckmarkOutline} /><strong>Planificá con tranquilidad</strong><span>Consultá horarios, elegí tu fecha y prepará la visita con anticipación.</span></article>
          </section>

          <section className="seccion-inicio galeria-seccion">
            <div className="cabecera-seccion"><div><span className="sobrelinea">INSPIRATE</span><h2>Un lugar para explorar.</h2></div><IonButton fill="clear" routerLink="/actividades" routerDirection="root">Ver actividades <IonIcon slot="end" icon={chevronDownOutline} /></IonButton></div>
            <div className="galeria-parque">
              <figure className="foto-parque foto-grande"><img src="/images/fondo.jpg" alt="Paisaje verde y tranquilo del parque" loading="lazy" /><figcaption><span>Naturaleza</span><strong>Encontrá tu lugar para desconectar</strong></figcaption></figure>
              <figure className="foto-parque foto-secundaria foto-uno"><img src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=900&q=85" alt="Sendero rodeado de árboles" loading="lazy" /><figcaption><span>Exploración</span><strong>Caminos por descubrir</strong></figcaption></figure>
              <figure className="foto-parque foto-secundaria foto-dos"><img src="https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=900&q=85" alt="Fauna en un entorno natural" loading="lazy" /><figcaption><span>Vida silvestre</span><strong>Pequeñas grandes maravillas</strong></figcaption></figure>
            </div>
            <p className="nota-fotos">Las fotografías externas son ilustrativas y representan paisajes naturales; no garantizan la presencia de especies o lugares específicos en el parque.</p>
          </section>

          <section className="datos-visita">
            <div className="dato-visita"><span className="dato-icono"><IonIcon icon={timeOutline} /></span><div><span>HORARIOS</span><strong>8:30 a 19:00</strong><small>Cerrado los lunes y feriados indicados.</small></div></div>
            <div className="dato-visita"><span className="dato-icono"><IonIcon icon={locationOutline} /></span><div><span>UBICACIÓN</span><strong>Consultá cómo llegar</strong><small>La dirección exacta se publicará en esta sección.</small></div></div>
            <div className="dato-visita"><span className="dato-icono"><IonIcon icon={peopleOutline} /></span><div><span>IDEAL PARA</span><strong>Familias y amigos</strong><small>Organizá una salida para compartir.</small></div></div>
          </section>

          <section className="seccion-inicio familia-panel">
            <div className="familia-copy"><span className="sobrelinea">UNA EXPERIENCIA PARA COMPARTIR</span><h2>Un día especial para grandes y chicos.</h2><p>Elegí las entradas según la edad de cada visitante. El sistema calcula automáticamente los descuentos correspondientes.</p><ul><li>Hasta 3 años: ingreso gratuito.</li><li>De 4 a 15 años: 50% de descuento.</li><li>Desde los 60 años: 50% de descuento.</li></ul><IonButton routerLink="/entradas" routerDirection="root">Planificar mi visita <IonIcon slot="end" icon={ticketOutline} /></IonButton></div>
            <div className="familia-imagen"><img src="https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?auto=format&fit=crop&w=1000&q=85" alt="Personas disfrutando de una salida al aire libre" loading="lazy" /></div>
          </section>

          <section className="seccion-inicio faq-seccion">
            <span className="sobrelinea">ANTES DE VENIR</span><h2>Preguntas frecuentes.</h2>
            <div className="faq-lista">{preguntas.map((p) => <details className="faq-item" key={p.q}><summary>{p.q}<IonIcon icon={chevronDownOutline} /></summary><p>{p.a}</p></details>)}</div>
          </section>

          <section className="seccion-inicio opiniones-seccion">
            <span className="sobrelinea">UNA EXPERIENCIA PARA RECORDAR</span><h2>Lo que nos gustaría que vivas.</h2>
            <p className="nota-fotos">Las siguientes opiniones son ejemplos de diseño y no corresponden a testimonios reales.</p>
            <div className="opiniones-grid"><article className="opinion-card"><div className="estrellas" aria-label="Cinco estrellas">★★★★★</div><p>“Un día para bajar el ritmo, caminar y disfrutar del verde en familia.”</p><span>Testimonio de demostración · Visitante familiar</span></article><article className="opinion-card"><div className="estrellas" aria-label="Cinco estrellas">★★★★★</div><p>“Me encanta la idea de tener un espacio para desconectar de la rutina.”</p><span>Testimonio de demostración · Amante de la naturaleza</span></article><article className="opinion-card"><div className="estrellas" aria-label="Cinco estrellas">★★★★★</div><p>“Planificar la visita con anticipación hace que todo sea más simple.”</p><span>Testimonio de demostración · Visitante</span></article></div>
          </section>

          <section className="cta-final"><div><span className="sobrelinea">TU PRÓXIMO RECUERDO EMPIEZA ACÁ</span><h2>La naturaleza te está esperando.</h2><p>Elegí tu fecha y prepará una nueva experiencia.</p></div><IonButton routerLink="/entradas" routerDirection="root" color="tertiary" size="large"><IonIcon slot="start" icon={ticketOutline} /> Comprar entradas</IonButton></section>
          {puedeInstalar && <IonCard><IonCardContent><h2>EcoHarmony, siempre cerca</h2><p>Instalá la app en tu dispositivo para tenerla siempre a mano.</p><IonButton expand="block" color="secondary" onClick={instalar}><IonIcon slot="start" icon={downloadOutline} /> Instalar app</IonButton></IonCardContent></IonCard>}
          <footer className="pie-inicio"><span>EcoHarmony Park</span><span>Naturaleza · aventura · bienestar</span><IonButton fill="clear" routerLink="/mapa" routerDirection="root"><IonIcon slot="start" icon={mapOutline} /> Mapa del parque</IonButton></footer>
        </div>
      </IonContent>
    </IonPage>
  );
};
export default Inicio;
