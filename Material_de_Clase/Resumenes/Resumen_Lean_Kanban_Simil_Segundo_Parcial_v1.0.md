# Lean y Kanban — Guía práctica para el parcial

> Pensada para el ejercicio típico: *"Dado este caso, identificá los tipos de trabajo, definí 5 políticas y diseñá el tablero Kanban"*.
> Basada en la Guía Oficial de Kanban, Essential Kanban Condensed, Kanban (Anderson), Kanban vs Scrum (Kniberg), Lean from the Trenches y Poppendieck.

---

## 1. Lo mínimo de teoría que tenés que poder decir

### Lean en 30 segundos
- Viene del **Sistema de Producción de Toyota**. Su objetivo es **entregar valor al cliente lo más rápido posible, eliminando desperdicio**.
- **7 principios** ("El Café Con Dulce Es Realmente Óptimo"): Eliminar desperdicio, Calidad integrada, Crear conocimiento, Diferir el compromiso, Entregar rápido, Respetar a las personas, Optimizar el todo.
- **7 desperdicios** ("Pedro Rompió Cinco Discos De Fito, Todos"): Pasamanos, Reaprendizaje, Cambio de tareas, Demoras, Defectos, Features extra, Trabajo parcialmente hecho.
- **Kanban es una forma concreta de aplicar Lean** al trabajo del conocimiento.

### Cómo se conecta Lean con Kanban (muy útil para justificar respuestas)

| Si en Kanban hacés... | ...estás aplicando este principio Lean | ...y atacás este desperdicio |
|---|---|---|
| Limitar el WIP | Entregar rápido / Optimizar el todo | Trabajo parcialmente hecho, Cambio de tareas |
| Sistema *pull* (tomar trabajo solo si hay lugar) | Diferir el compromiso | Features extra, Trabajo a medias |
| Visualizar el flujo y los bloqueos | Crear conocimiento / Optimizar el todo | Demoras |
| Criterios de "terminado" por columna con pruebas | Calidad integrada | Defectos |
| Políticas explícitas escritas junto al tablero | Crear conocimiento / Respetar a las personas | Reaprendizaje |
| Equipos que se autoorganizan alrededor del tablero | Respetar a las personas | Pasamanos |
| Medir lead time y mejorar con datos | Optimizar el todo / Entregar rápido | Demoras |

### Kanban en 30 segundos
- Es un **método** (no metodología ni framework) que se aplica **sobre el proceso que ya existe**. "Empezá con lo que hacés ahora".
- **Principios de gestión del cambio:** comenzar con lo que hacés ahora, acordar la mejora evolutiva, fomentar el liderazgo en todos los niveles.
- **Principios de entrega del servicio:** enfocarse en el cliente, gestionar el trabajo (no a las personas), revisar la red de servicios y sus políticas.
- **6 prácticas** ("Vamos Lento, Ganando Partidos Con Messi"): Visualizar, Limitar el WIP, Gestionar el flujo, Políticas explícitas, Ciclos de retroalimentación, Mejorar colaborativamente.
- **Métricas:** lead time, throughput (tasa de entrega), WIP, CFD. **Ley de Little:** Lead time = WIP / Throughput.

---

## 2. Cosas importantes a tener en cuenta (lo que suele corregir el profe)

1. **El tablero modela el proceso REAL, no el ideal.** No pongas "Pendiente / Haciendo / Hecho" y listo: poné las etapas reales del caso (análisis, desarrollo, testing, etc.).
2. **Las columnas son etapas del trabajo, no personas ni roles.** Nada de columnas "Juan" o "Tester".
3. **Las tarjetas son ítems de trabajo que entregan valor** (una historia, un bug, un cambio), no tareas personales tipo "hacer el café".
4. **Todas las columnas intermedias llevan límite de WIP.** El backlog / entrada y la columna final "Terminado / En producción" normalmente **no** llevan límite (el backlog a veces lleva uno para no acumular, pero eso es opcional).
5. **Dividí las etapas en "En curso" y "Hecho"** (subcolumnas). El límite de WIP abarca **las dos juntas**. La subcolumna "Hecho" es la que hace visible el *pull*: el trabajo espera ahí hasta que la etapa siguiente lo tome.
6. **Marcá el punto de compromiso** (cuando el ítem entra en "Listo para comenzar" o "Próximo": desde ahí corre el **lead time**) y el **punto de entrega**.
7. **Justificá los límites de WIP** con la capacidad: por ejemplo, la cantidad de personas en esa etapa (o personas + 1). Decí también que se **ajustan empíricamente**.
8. **Las políticas tienen que ser concretas y verificables.** "Trabajar bien" no es una política; "Un ítem pasa a Testing solo si tiene code review aprobado y los tests unitarios en verde" sí lo es.
9. **Expedite (urgente) con límite propio, normalmente 1**, y una regla clara de qué califica como urgente. Si no, todo termina siendo urgente.
10. **Visualizá los bloqueos** (tarjeta roja o un ícono) y definí una política para tratarlos.
11. **Kanban no prescribe roles, iteraciones ni estimaciones.** No metas sprints ni Scrum Master salvo que el caso los tenga (y si los tiene, Kanban se suma a lo que ya hay).
12. **Diferenciá tipos de trabajo de clases de servicio.** El *tipo* es *qué* es (bug, feature, mejora); la *clase de servicio* es *cómo se trata* (expedite, fecha fija, estándar, intangible). Un bug puede ser estándar o expedite según su impacto.

---

## 3. Receta para resolver el ejercicio (paso a paso)

Es una versión simplificada de **STATIK**. Seguí este orden y nunca te va a faltar nada:

1. **Entender el servicio:** quién es el cliente, qué pide, de qué se queja hoy (fuentes de insatisfacción).
2. **Tipos de trabajo:** listá de 4 a 6, cada uno con origen, tamaño típico y un ejemplo.
3. **Flujo de trabajo:** las etapas por las que pasa cada tipo. Esas son las columnas.
4. **Clases de servicio:** cómo se trata cada tipo (expedite / fecha fija / estándar / intangible).
5. **Límites de WIP:** por columna, justificados con la capacidad del equipo.
6. **Políticas explícitas (5 o más):** de WIP, de pull / Definition of Done por columna, de clases de servicio, de reposición y de bloqueos.
7. **Dibujar el tablero:** columnas, subcolumnas, WIP, carriles (*swimlanes*), punto de compromiso y algunas tarjetas de ejemplo.
8. **Cerrar con métricas y cadencias** (aunque no lo pidan, suma): lead time, throughput, CFD; daily frente al tablero, reunión de reposición y retrospectiva.

### Tipos de políticas que te conviene cubrir (así llegás fácil a 5)

| Tipo de política | Pregunta que responde | Ejemplo |
|---|---|---|
| **Límite de WIP** | ¿Cuántos ítems puede haber en cada etapa? | "Desarrollo admite como máximo 4 ítems entre En curso y Hecho." |
| **Criterio de pull / DoD de la columna** | ¿Cuándo un ítem está listo para pasar a la siguiente? | "Pasa a Testing solo con code review aprobado y tests unitarios en verde." |
| **Clase de servicio** | ¿Quién tiene prioridad y bajo qué condiciones? | "Expedite: solo caídas en producción; límite 1; puede superar el WIP; lo toma la primera persona que se libera." |
| **Reposición / priorización** | ¿Quién elige qué entra y cuándo? | "El PO repone la columna Próximo los lunes; dentro de la columna se toma de arriba hacia abajo." |
| **Bloqueos** | ¿Qué hacemos si un ítem se traba? | "Si un ítem está bloqueado más de 1 día se marca en rojo y se trata primero en la daily." |
| **Reglas del equipo** | ¿Cómo trabajamos día a día? | "Antes de tomar algo nuevo, ayudo a terminar algo de mi columna o de la siguiente (empezar a terminar)." |

---

## 4. Ejemplo resuelto 1 — Equipo de mantenimiento de un sistema de turnos de una clínica

### El caso
Una software factory mantiene el **sistema de turnos online de una clínica**, que ya está en producción. El equipo tiene **1 analista funcional, 4 desarrolladores y 2 testers**, y el líder de proyecto cumple el rol de referente del cliente. Llegan pedidos por mail, por teléfono y por la mesa de ayuda. Hoy el cliente se queja de que "nunca sabe cuándo va a estar lo que pidió" y de que "los errores urgentes tardan días". El equipo se queja de que lo interrumpen todo el tiempo y de que arranca muchas cosas sin terminar ninguna.

### 4.1 Fuentes de insatisfacción
- **Cliente:** falta de previsibilidad y urgencias que tardan demasiado.
- **Equipo:** interrupciones constantes, multitarea y demasiado trabajo empezado.
→ Kanban ayuda con **WIP limitado** (menos multitarea), **clase expedite** (urgencias rápidas) y **lead time medido** (previsibilidad).

### 4.2 Tipos de trabajo

| Tipo | Ejemplo | Tamaño típico | Origen |
|---|---|---|---|
| **Incidente en producción** | "Los pacientes no pueden reservar turnos desde el celular" | Chico, pero crítico | Mesa de ayuda |
| **Corrección de defecto** | "El mail de confirmación muestra mal la hora" | Chico | Mesa de ayuda / testing |
| **Nueva funcionalidad** | "Permitir reprogramar un turno desde la app" | Mediano/grande (se divide en historias) | Clínica |
| **Mejora** | "Agregar filtro por obra social en la búsqueda de médicos" | Chico/mediano | Clínica / usuarios |
| **Cambio normativo** | "Adaptar la receta electrónica a la nueva resolución del Ministerio de Salud antes del 1/3" | Mediano, **con fecha límite** | Externo (regulación) |
| **Deuda técnica** | "Actualizar la versión del framework; refactorizar el módulo de agenda" | Mediano | Equipo |

### 4.3 Clases de servicio

| Clase | Qué tipos entran | Tratamiento |
|---|---|---|
| **Expedite (urgente)** | Incidentes en producción que impiden reservar o atender | Carril propio, **límite 1**, puede superar el WIP de las columnas, se atiende de inmediato |
| **Fecha fija** | Cambios normativos | Se priorizan según la fecha; se empiezan con margen (ej. 3 semanas antes) |
| **Estándar** | Funcionalidades, mejoras, defectos no críticos | Por orden de prioridad del backlog (FIFO dentro de la columna Próximo) |
| **Intangible** | Deuda técnica | Se reserva capacidad fija: 1 de cada 5 ítems que entran (~20%) |

### 4.4 Flujo de trabajo (columnas)
**Entrada (Backlog) → Próximo [punto de compromiso] → Análisis → Desarrollo → Testing → Listo para producción → En producción [punto de entrega]**

### 4.5 Límites de WIP (justificados)

| Columna | WIP | Justificación |
|---|---|---|
| Entrada | — (sin límite) | Es la lista de opciones; todavía no hay compromiso |
| Próximo | 4 | Lo que el equipo puede tomar en ~1 semana; evita compromisos de más |
| Análisis | 2 | 1 analista: 1 en curso + 1 esperando en "Hecho" |
| Desarrollo | 4 | 4 desarrolladores, 1 ítem cada uno |
| Testing | 3 | 2 testers + 1 de margen para que Desarrollo no se frene |
| Listo para producción | 3 | Se despliega 2 veces por semana; evita acumular sin entregar |
| En producción | — | Es la salida |
| **Carril Expedite** | **1** | Solo una urgencia a la vez |

> Los límites son un punto de partida: se revisan en la retrospectiva con los datos del CFD y del lead time.

### 4.6 Políticas explícitas (con las 5 ya cumplís, acá hay 7)

1. **WIP:** no se puede pasar un ítem a una columna que alcanzó su límite (sumando En curso + Hecho). Si tu columna está llena, ayudás a destrabar la siguiente.
2. **Criterio de entrada a Próximo (Definition of Ready):** el ítem tiene descripción, criterios de aceptación acordados con la clínica y, si es una funcionalidad, está dividido en partes que se pueden terminar en menos de 1 semana.
3. **Criterio de salida de Desarrollo:** el código tiene **code review aprobado**, **tests unitarios en verde** y está integrado en la rama principal (el build de integración continua pasa).
4. **Criterio de salida de Testing:** se ejecutaron los casos de prueba de los criterios de aceptación y la **regresión automatizada**, sin defectos de severidad alta abiertos.
5. **Expedite:** solo califica un incidente que **impide a pacientes o médicos usar el sistema**. Lo confirma el líder de proyecto. Límite 1. Lo toma el primer desarrollador que termina su ítem actual (no se abandona trabajo a medias salvo caída total). Se despliega apenas pasa el testing de humo.
6. **Reposición:** el líder de proyecto, junto con la clínica, repone **Próximo** en la reunión de reposición de los lunes. Dentro de Próximo se toma de arriba hacia abajo, excepto si hay un ítem de fecha fija en riesgo.
7. **Bloqueos:** un ítem bloqueado (por ejemplo, esperando una respuesta de la clínica) se marca con una etiqueta roja indicando motivo y fecha. Si pasa más de 2 días bloqueado, el líder lo escala. Los ítems bloqueados **cuentan** para el WIP (para que duelan y se resuelvan).

### 4.7 Tablero

```
 ENTRADA      | PRÓXIMO (4)  || ANÁLISIS (2)     | DESARROLLO (4)       | TESTING (3)          | LISTO P/ PROD (3) | EN PRODUCCIÓN
 (sin límite) |              || En curso | Hecho | En curso    | Hecho  | En curso     | Hecho |                   |
==============|==============||==================|======================|======================|===================|===============
 EXPEDITE (1) |              ||                  | [INC-12 No se        |                      |                   |
              |              ||                  |  reservan turnos     |                      |                   |
              |              ||                  |  desde celular] !!   |                      |                   |
--------------|--------------||------------------|----------------------|----------------------|-------------------|---------------
 FECHA FIJA   | [NORM-3      ||                  | [NORM-2 Receta       |                      |                   |
              |  Resol. 1/3] ||                  |  electr. vence 1/3]  |                      |                   |
--------------|--------------||------------------|----------------------|----------------------|-------------------|---------------
 ESTÁNDAR     | [FUN-8       || [FUN-7  | [MEJ-4 | [FUN-5]     | [DEF-9]| [FUN-3]      |       | [MEJ-2 Filtro     | [FUN-1]
 [FUN-10]     |  Reprogramar || Recorda-| Filtro | [DEF-11]    |        | [DEF-6]      |       |  obra social]     | [DEF-2]
 [MEJ-6]      |  turno]      || torio   | por    |   (BLOQ:    |        |              |       |                   | [MEJ-1]
 [DEF-13]     | [DEF-12]     || SMS]    | sede]  |   espera    |        |              |       |                   |
              |              ||         |        |   clínica)  |        |              |       |                   |
--------------|--------------||------------------|----------------------|----------------------|-------------------|---------------
 INTANGIBLE   | [DT-1 Refac- ||                  |                      |                      |                   |
 [DT-2 Actua- |  tor módulo  ||                  |                      |                      |                   |
  lizar fwk]  |  agenda]     ||                  |                      |                      |                   |
              ^              ^                                                                                    ^
              |              PUNTO DE COMPROMISO (empieza a correr el lead time)                PUNTO DE ENTREGA --
```

**Cómo leerlo:**
- Hay **carriles (swimlanes)** por clase de servicio y **colores o prefijos por tipo de trabajo**: INC = incidente, DEF = defecto, FUN = funcionalidad, MEJ = mejora, NORM = normativo, DT = deuda técnica.
- **Conteo de WIP (hacelo siempre antes de entregar):** Próximo = FUN-8, DEF-12, NORM-3, DT-1 → 4/4. Análisis = FUN-7, MEJ-4 → 2/2. Desarrollo = NORM-2, FUN-5, DEF-11, DEF-9 → 4/4, más INC-12, que está en el carril expedite y por política puede superar el límite. Testing = FUN-3, DEF-6 → 2/3. Listo para producción = MEJ-2 → 1/3.
- Como Próximo está lleno, DT-2 espera en Entrada. Como Desarrollo está lleno, MEJ-4 no puede avanzar aunque su análisis esté terminado: así se ve el **pull**.
- **DEF-11** está **bloqueado** (esperando respuesta de la clínica) y cuenta para el WIP.
- **MEJ-4** está en *Análisis / Hecho*: terminó el análisis y espera que Desarrollo tenga lugar para hacer *pull*.

### 4.8 Métricas y cadencias para este caso
- **Lead time por clase de servicio** (ej.: "el 85% de los ítems estándar se entregan en 10 días o menos"). Con esto se le responde a la clínica "¿cuándo va a estar?". Ataca la queja principal.
- **Throughput semanal**, **CFD** (para ver si Testing es un cuello de botella), **cantidad de ítems bloqueados y días bloqueados**, **cumplimiento de fechas** para los normativos.
- **Cadencias:** reunión diaria de 15 min frente al tablero, recorriéndolo **de derecha a izquierda** (primero lo más cercano a terminar); **reposición** los lunes; **planificación de entregas** (despliegues martes y jueves); **retrospectiva** quincenal para revisar límites y políticas.

---

## 5. Ejemplo resuelto 2 — Startup que desarrolla una app de delivery

### El caso
Un equipo de **6 personas** (1 UX, 4 desarrolladores full-stack, 1 QA) desarrolla una **app nueva de pedidos para restaurantes**. El dueño del producto quiere salir rápido al mercado con un **MVP** e ir agregando funcionalidades según el uso real.

**Tipos de trabajo:** historia de usuario ("Como cliente quiero pagar con Mercado Pago"), experimento / hipótesis ("Si mostramos un descuento en el primer pedido, la conversión sube un 10%"), defecto, spike técnico (investigación con timebox: "evaluar mapas de Google vs OpenStreetMap"), tarea de infraestructura (configurar el pipeline de despliegue continuo).

**Flujo:** Ideas → Próximo (compromiso) → Diseño UX → Desarrollo → QA → Producción → **Validación con métricas** (¿se cumplió la hipótesis?) → Terminado.
> El paso "Validación" es la parte Lean (Lean UX: construir → medir → aprender). Algo está terminado cuando **se aprendió algo**, no solo cuando se desplegó.

**WIP:** Próximo 3 · Diseño UX 2 · Desarrollo 4 · QA 2 · Validación 3.

**5 políticas:**
1. Una historia entra a Próximo solo si tiene la **hipótesis y la métrica de éxito** definidas.
2. Desarrollo termina con tests automáticos y el **pipeline de CI en verde**; se despliega detrás de un *feature toggle*.
3. QA prueba en el ambiente de staging con dispositivos Android e iOS; los defectos críticos vuelven a Desarrollo **en la misma tarjeta** (no se abren tarjetas nuevas).
4. Un ítem sale de Validación cuando pasaron **7 días** de datos reales; si la hipótesis falla, se crea una tarjeta para **quitar la funcionalidad** (evitar features extra).
5. Los spikes tienen un **timebox de 2 días** y un límite de 1 a la vez.

**Desperdicios Lean que se atacan:** *features extra* (con validación de hipótesis), *demoras* (despliegue continuo), *trabajo parcialmente hecho* (WIP bajo).

---

## 6. Ejemplo rápido 3 — Para practicar: el TP de una materia (3 alumnos)
- **Tipos de trabajo:** entregable del TP, investigación teórica, código, corrección de una devolución del profe, armado de la presentación.
- **Columnas:** Pendiente → Próximo (WIP 3) → Haciendo (WIP 3, uno por persona) → Revisión del compañero (WIP 2) → Listo para entregar → Entregado.
- **Clases de servicio:** *fecha fija* = las entregas al profe; *estándar* = el resto; *expedite* = la corrección pedida para mañana.
- **Políticas:** nadie tiene más de 1 tarjeta en Haciendo; todo pasa por la revisión de otro integrante antes de quedar listo; se repone Próximo los domingos; si alguien se traba más de 1 día, avisa en el grupo.

Sirve para practicar la receta con un caso que conocés bien.

---

## 7. Errores típicos (a evitar en el parcial)

| Error | Por qué está mal | Cómo hacerlo |
|---|---|---|
| Tablero "To Do / Doing / Done" genérico | No modela el proceso real del caso | Usar las etapas reales del enunciado |
| Sin límites de WIP | Sin WIP no hay sistema pull: sería un tablero visual, no Kanban | Poner un número en cada columna intermedia |
| WIP sin justificar | Parece arbitrario | Relacionarlo con las personas o la capacidad de la etapa |
| Políticas vagas ("comunicarse bien") | No se pueden verificar | Escribir condiciones concretas (qué, quién, cuándo, cuánto) |
| Columnas por persona | Se gestionan personas, no trabajo | Columnas = etapas del flujo |
| Meter sprints, Scrum Master y story points | Kanban no los prescribe | Solo si el caso ya los usa ("empezar con lo que hacés ahora") |
| Confundir tipo de trabajo con clase de servicio | Son dos dimensiones distintas | Tipo = qué es; clase = cómo se trata |
| El ejemplo de tablero supera los WIP que vos mismo definiste | Contradicción interna | Contar las tarjetas de cada columna antes de entregar |
| No marcar el punto de compromiso | No se sabe desde dónde se mide el lead time | Marcarlo en "Próximo" |
| Hablar de "velocidad" como métrica principal | Esa es la métrica de Scrum | En Kanban, la principal es el lead time |

---

## 8. Plantilla de respuesta (para copiar la estructura en el parcial)

1. **Contexto y problemas actuales** (2–3 líneas).
2. **Tipos de trabajo** (tabla: tipo, ejemplo, origen).
3. **Clases de servicio** (y qué tipo va en cada una).
4. **Flujo / columnas**, con el punto de compromiso y el de entrega.
5. **Límites de WIP** con la justificación.
6. **Políticas explícitas** (al menos 5, cubriendo WIP, pull/DoD, clases de servicio, reposición y bloqueos).
7. **Tablero dibujado** con carriles, subcolumnas En curso/Hecho y tarjetas de ejemplo **que respeten el WIP**.
8. **Métricas y cadencias** (lead time, throughput, CFD; daily, reposición, retrospectiva).
9. **Una línea Lean**: qué desperdicios ataca esta propuesta y por qué.
