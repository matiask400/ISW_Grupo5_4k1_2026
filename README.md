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


## ⚙ Configuración del repositorio

Los ítems de configuración, su ubicación y reglas de nombrado se detallan en `Descripcion_CI.md`. Como criterio general:

| Ítem de configuración | Unidad de control | Regla de nombrado | Extensiones permitidas |
| --- | --- | --- | --- |
| Material provisto por cátedra | Archivo dentro de su directorio temático | Se conserva el nombre oficial | `.pdf`, `.docx`, `.xlsx`, `.pptx` |
| Resumen grupal | Archivo | `Resumen_<Tema>_v<MAJOR>.<MINOR>.md` | `.md`, `.pdf` |
| Artefacto de TP | Archivo | `TP_<NN>_<Artefacto>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx` |
| Retroalimentación | Archivo | `TP_<NN>_Retroalimentacion_<AAAA-MM-DD>.<ext>` | `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg` |
| Evidencia del repositorio | Archivo | `TP_<NN>_Evidencia_<Descripcion>_<AAAA-MM-DD>.<ext>` | `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg` |


### Glosario

- `<NN>`: número de dos dígitos del TP o secuencia, por ejemplo `04` o `05`.
- `<Tema>`: título breve usando `_` como separador.
- `<Artefacto>`: tipo de documento, por ejemplo `Resolucion`, `Informe`, `Checklist` o `Cronograma`.
- `<AAAA-MM-DD>`: fecha ISO 8601.
- `<ext>`: una extensión admitida para ese ítem.
- `v<MAJOR>.<MINOR>`: versión del artefacto. `MAJOR` aumenta ante una entrega nueva o un cambio estructural importante; `MINOR`, ante ajustes dentro de la misma entrega.

## Líneas base
Se definirá una nueva línea base después de cada parcial evaluativo. 
Este criterio se adopta porque los parciales constituyen hitos de referencia que permiten evaluar y comparar el progreso del grupo a lo largo de la asignatura.
Cada línea base tiene un nombre con la siguiente nomenclatura: v[MAJOR].[MINOR]

| Nombre | Fecha | Descripción |
| --- | --- | --- |
| v1.0 | 05/09/2026 | Primer Parcial rendido el 03/09/2026  |
| v2.0 | 03/10/2026 | Segundo Parcial rendido el 31/10/2026 |
| v3.0 | 30/11/2026 | Recuperatorio rendido el 28/11/2026   |
