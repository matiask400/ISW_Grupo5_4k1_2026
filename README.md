# ISW_Grupo5_4k1_2026

Repositorio del Grupo 5 de la asignatura **Ingeniería y Calidad de Software**, año 2026, curso 4K1.

## Integrantes del grupo

| Nombre | Legajo | Mail |
| --- | ---: | --- |
| Gaspar Brocanelli | 400989 | [gaspibroca@gmail.com](mailto:gaspibroca@gmail.com) |
| Matías Adolfo Koroch | 96369 | [96369@sistemas.frc.utn.edu.ar](mailto:96369@sistemas.frc.utn.edu.ar) |
| Baltasar Gaitán Acevedo | 401077 | [baltasargaitan12@gmail.com](mailto:baltasargaitan12@gmail.com) |
| Felipe Vilchez | 95178 | [vilchez320@gmail.com](mailto:vilchez320@gmail.com) |
| Lautaro Comas | 96586 | [lautaroacomas@gmail.com](mailto:lautaroacomas@gmail.com) |
| Abril Salinas | 94243 | [abrilsalinas2003@gmail.com](mailto:abrilsalinas2003@gmail.com) |
| Mateo Sanchez | 91785 | [sanchezmateo090@gmail.com](mailto:sanchezmateo090@gmail.com) |
| Mayra Morellato | 97325 | [mayra.m2230@gmail.com](mailto:mayra.m2230@gmail.com) |
| Manuel Fassi | 98518 | [fassimanu@gmail.com](mailto:fassimanu@gmail.com) |
| Luciano Tissera | 99236 | [ltissera17@gmail.com](mailto:ltissera17@gmail.com) |
| María Lucía Romero Peñaloza | 95694 | [romeropenalozal26@gmail.com](mailto:romeropenalozal26@gmail.com) |
| Martín Imoberdorf | 91570 | [tinchoimo@gmail.com](mailto:tinchoimo@gmail.com) |
| Bianca Xiomara Hermoza | 95578 | [biancaxiomarah@gmail.com](mailto:biancaxiomarah@gmail.com) |

## Estructura del repositorio

```text
ISW_Grupo5_4k1_2026/
├── Material_de_Clase/
│   ├── Bibliografia/
│   ├── Guias/
│   ├── Planificacion/
│   ├── Presentaciones_Teoricas/
│   ├── Resumenes/
│   └── Templates/
├── Notas/
│   ├── Teorico/
│   └── Practico/
├── Trabajos_Practicos/
│   ├── Investigacion/
│   └── Evaluables/
├── README.md
└── .gitignore
```

`Material_de_Clase/Planificacion/` es un directorio que agrupa el cronograma, programa de la asignatura y material de seguimiento. `Trabajos_Practicos/` también es un directorio contenedor: cada TP evaluable se registra en un subdirectorio independiente y todos comparten la misma estructura interna. Esto permite incorporar nuevos TPs sin cambiar el criterio de organización.

## Flujo de los trabajos prácticos

Cada `TP_<NN>_<Tema>/` conserva las siguientes entradas y salidas:

| Directorio | Contenido | Rol |
| --- | --- | --- |
| `00_Enunciado/` | Consigna, guía, aclaraciones y material provisto por la cátedra | Entrada |
| `01_Produccion/` | Artefactos de trabajo del grupo, incluyendo código fuente si corresponde | Trabajo en curso |
| `02_Entrega/` | Versión final presentada | Salida formal |
| `03_Retroalimentacion/` | Correcciones, calificaciones y devoluciones recibidas | Entrada posterior |
| `04_Evidencias_Repositorio/` | Capturas, reportes de Git, tags y pruebas de actualización | Evidencia de gestión |

Las carpetas se mantienen incluso cuando un TP no requiere contenido en alguna de ellas; así se preserva la consistencia entre entregas.

## Ítems de configuración y nomenclatura

Los ítems de configuración, su ubicación y reglas de nombrado se detallan en `Descripcion_CI.md`. Como criterio general:

| Ítem | Unidad de control | Nombre | Extensiones permitidas |
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
