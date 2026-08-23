# ISW_Grupo5_4k1_2026

Repositorio del Grupo 5 de la asignatura **Ingeniería y Calidad de Software**, año 2026, curso 4K1.

## 👥 Integrantes del grupo

| Nombre | Legajo | Mail |
| --- | --- | --- |
| Brocanelli, Gaspar | 400989 | [gaspibroca@gmail.com](mailto:gaspibroca@gmail.com) |
| Comas, Lautaro | 96586 | [lautaroacomas@gmail.com](mailto:lautaroacomas@gmail.com) |
| Fassi, Manuel | 98518 | [fassimanu@gmail.com](mailto:fassimanu@gmail.com) |
| Gaitán Acevedo, Baltasar | 401077 | [baltasargaitan12@gmail.com](mailto:baltasargaitan12@gmail.com) |
| Hermoza, Bianca Xiomara | 95578 | [biancaxiomarah@gmail.com](mailto:biancaxiomarah@gmail.com) |
| Imoberdorf, Martín José | 91570 | [tinchoimo@gmail.com](mailto:tinchoimo@gmail.com) |
| Koroch, Matías Adolfo | 96369 | [96369@sistemas.frc.utn.edu.ar](mailto:96369@sistemas.frc.utn.edu.ar) |
| Morellato, Mayra | 97325 | [mayra.m2230@gmail.com](mailto:mayra.m2230@gmail.com) |
| Romero Peñaloza, María Lucía | 95694 | [romeropenalozal26@gmail.com](mailto:romeropenalozal26@gmail.com) |
| Salinas, Abril | 94243 | [abrilsalinas2003@gmail.com](mailto:abrilsalinas2003@gmail.com) |
| Sanchez, Mateo | 91785 | [sanchezmateo090@gmail.com](mailto:sanchezmateo090@gmail.com) |
| Tissera, Luciano | 99236 | [ltissera17@gmail.com](mailto:ltissera17@gmail.com) |
| Vilchez, Felipe | 95178 | [vilchez320@gmail.com](mailto:vilchez320@gmail.com) |

## 📝 Estructura del repositorio

```text
ISW_Grupo5_4k1_2026/
├── Material_de_Clase/
│   ├── Bibliografia/
│   ├── Guias/
│   ├── Planificacion/
│   ├── Presentaciones_Teoricas/
│   ├── Resumenes/
│   └── Templates/
│   └── Link Clases Grabadas/
├── Notas/
│   ├── Teorico/
│   └── Practico/
├── Trabajos_Practicos/
│   ├── Investigacion/
│   └── Evaluables/
├── README.md
└── .gitignore
```
## Criterios de Organizacion
* `Material_de_Clase/Bibliografia/` es un directorio donde se encuentra la bibliografia para cada unidad de la asignatura.
* `Material_de_Clase/Guias/` es un directorio donde se encuetran las guias de ejercicios practicos y sus soluciones.
* `Material_de_Clase/Planificacion/` es un directorio que agrupa el cronograma, programa de la asignatura y material de seguimiento. 
* `Material_de_Clase/Presentaciones_Teoricas/` es un directorio donde se encuentran las presentaciones power point del desarrollo de la asginatura.
* `Material_de_Clase/Resumenes/` es un directorio donde se encuentran los resumenes para el estudio de la asignatura realizados por los estudiantes.
* `Notas/` es un directorio donde se encuentran las anotaciones realizadas en clases por los estudiantes.
* `Trabajos_Practicos/` es un directorio contenedor: cada TP evaluable se registra en un subdirectorio independiente y todos comparten la misma estructura interna. Esto permite incorporar nuevos TPs sin cambiar el criterio de organización.


## ⚙ Ítems de configuración

| Ítem de configuración | Unidad de control | Regla de nombrado | Extensiones permitidas | Ubicación | Tipo |
| --- | --- | --- | --- | --- | --- |
| **Bibliografía** | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.pdf` | `Material_de_Clase/Bibliografia/` | Recurso de cátedra |
| **Guías de ejercicios** | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.pdf`, `.docx` | `Material_de_Clase/Guias/` | Recurso de cátedra |
| **Planificación** | Directorio y archivos contenidos | `Planificacion_<Tema>.<ext>` para material del grupo; nombre oficial para material de cátedra | `.md`, `.pdf`, `.xlsx` | `Material_de_Clase/Planificacion/` | Recurso de cátedra / material propio |
| **Presentaciones teóricas** | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.pdf`, `.pptx` | `Material_de_Clase/Presentaciones_Teoricas/` | Recurso de cátedra |
| **Resúmenes** | Archivo | `Resumen_<Tema>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf` | `Material_de_Clase/Resumenes/` | Material propio |
`Material_de_Clase/Templates/` | Recurso de cátedra |
| **Trabajo práctico** | Directorio | `TP_<NN>_<Tema>/` | No aplica | `Trabajos_Practicos/` | Material propio |
| **Enunciado de TP** | Archivo | Se conserva el nombre oficial provisto | `.pdf`, `.docx` | `Trabajos_Practicos/TP_<NN>_<Tema>/00_Enunciado/` | Recurso de cátedra |
| **Producción de TP** | Archivo | `TP_<NN>_<Artefacto>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx` | `Trabajos_Practicos/TP_<NN>_<Tema>/01_Produccion/` | Material propio |
| **Código fuente** | Directorio y archivos contenidos | Convenciones propias del lenguaje o tecnología | Según tecnología | `Trabajos_Practicos/TP_<NN>_<Tema>/01_Produccion/Codigo_Fuente/` | Material propio |
| **Entrega de TP** | Archivo | `TP_<NN>_<Artefacto>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx` | `Trabajos_Practicos/TP_<NN>_<Tema>/02_Entrega/` | Material propio |
| **Retroalimentación** | Archivo | `TP_<NN>_Retroalimentacion_<AAAA-MM-DD>.<ext>` | `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg` | `Trabajos_Practicos/TP_<NN>_<Tema>/03_Retroalimentacion/` | Recurso de cátedra |
| **Evidencia de repositorio** | Archivo | `TP_<NN>_Evidencia_<Descripcion>_<AAAA-MM-DD>.<ext>` | `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg` | `Trabajos_Practicos/TP_<NN>_<Tema>/04_Evidencias_Repositorio/` | Material propio |
| **Documento de estructura SCM** | Archivo | `README.md` | `.md` | Raíz del repositorio | Documento de gestión |


## 🔁 Flujo de los trabajos prácticos

Cada `TP_<NN>_<Tema>/` conserva las siguientes entradas y salidas:

| Directorio | Contenido | Rol |
| --- | --- | --- |
| `00_Enunciado/` | Consigna, guía, aclaraciones y material provisto por la cátedra | Entrada |
| `01_Produccion/` | Artefactos de trabajo del grupo, incluyendo código fuente si corresponde | Trabajo en curso |
| `02_Entrega/` | Versión final presentada | Salida formal |
| `03_Retroalimentacion/` | Correcciones, calificaciones y devoluciones recibidas | Entrada posterior |
| `04_Evidencias_Repositorio/` | Capturas, reportes de Git, tags y pruebas de actualización | Evidencia de gestión |

### 🗒️ Glosario

- `<NN>`: número de dos dígitos del TP, por ejemplo `04` o `05`.
- `<Tema>`: título breve usando `_` como separador. 
- `<Artefacto>`: tipo de documento, por ejemplo `Resolucion`, `Informe`, `Cronograma`.
- `<AAAA-MM-DD>`: fecha en formato ISO 8601.
- `<ext>`:  extensión permitida para el ítem de configuración.
- `v<MAJOR>.<MINOR>`: versión del artefacto. `MAJOR` aumenta ante una entrega nueva o un cambio estructural importante; `MINOR`, ante ajustes dentro de la misma entrega.

## Líneas base
Se definirá una nueva línea base después de cada parcial evaluativo. 
Utilizaremos cada examen parcial como un hito clave dentro de la gestión de configuración de software, lo que nos permitirá medir avances, consolidar cambios y garantizar la estabilidad de la versión en el repositorio.
Cada línea base tiene un nombre con la siguiente nomenclatura: v[MAJOR].[MINOR]

| Nombre | Fecha | Descripción |
| --- | --- | --- |
| v1.0 | 05/09/2026 | Fecha primer parcial 03/09/2026  |
| v2.0 | 03/10/2026 | Fecha segundo parcial 31/10/2026 |
| v3.0 | 30/11/2026 | Fecha recuperatorio 28/11/2026   |
