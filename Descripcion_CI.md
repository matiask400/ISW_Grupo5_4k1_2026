# Descripción de ítems de configuración

Este documento define los ítems de configuración (CI) del repositorio, su ubicación física, las extensiones admitidas y las reglas de nombrado.

| Ítem de configuración | Unidad de control | Regla de nombrado | Extensiones permitidas | Ubicación | Tipo |
| --- | --- | --- | --- | --- | --- |
| Bibliografía | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.pdf` | `Material_de_Clase/Bibliografia/` | Recurso de cátedra |
| Guías y enunciados generales | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.pdf`, `.docx` | `Material_de_Clase/Guias/` | Recurso de cátedra |
| Planificación | Directorio y archivos contenidos | `Planificacion_<Tema>.<ext>` para material del grupo; nombre oficial para material de cátedra | `.md`, `.pdf`, `.xlsx` | `Material_de_Clase/Planificacion/` | Recurso de cátedra / material propio |
| Presentaciones teóricas | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.pdf`, `.pptx` | `Material_de_Clase/Presentaciones_Teoricas/` | Recurso de cátedra |
| Resúmenes | Archivo | `Resumen_<Tema>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf` | `Material_de_Clase/Resumenes/` | Material propio |
| Plantillas | Directorio y archivos contenidos | Se conserva el nombre oficial provisto | `.docx`, `.xlsx`, `.md`, `.pdf` | `Material_de_Clase/Templates/` | Recurso de cátedra |
| Trabajo práctico | Directorio | `TP_<NN>_<Tema>/` | No aplica | `Trabajos_Practicos/` | Material propio |
| Enunciado de TP | Archivo | Se conserva el nombre oficial provisto | `.pdf`, `.docx` | `Trabajos_Practicos/TP_<NN>_<Tema>/00_Enunciado/` | Recurso de cátedra |
| Producción de TP | Archivo | `TP_<NN>_<Artefacto>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx` | `Trabajos_Practicos/TP_<NN>_<Tema>/01_Produccion/` | Material propio |
| Código fuente | Directorio y archivos contenidos | Convenciones propias del lenguaje o tecnología | Según tecnología | `Trabajos_Practicos/TP_<NN>_<Tema>/01_Produccion/Codigo_Fuente/` | Material propio |
| Entrega de TP | Archivo | `TP_<NN>_<Artefacto>_v<MAJOR>.<MINOR>.<ext>` | `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx` | `Trabajos_Practicos/TP_<NN>_<Tema>/02_Entrega/` | Material propio |
| Retroalimentación | Archivo | `TP_<NN>_Retroalimentacion_<AAAA-MM-DD>.<ext>` | `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg` | `Trabajos_Practicos/TP_<NN>_<Tema>/03_Retroalimentacion/` | Recurso de cátedra |
| Evidencia de repositorio | Archivo | `TP_<NN>_Evidencia_<Descripcion>_<AAAA-MM-DD>.<ext>` | `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg` | `Trabajos_Practicos/TP_<NN>_<Tema>/04_Evidencias_Repositorio/` | Material propio |
| Documento de estructura SCM | Archivo | `README.md` | `.md` | Raíz del repositorio | Documento de gestión |
| Tabla de ítems de configuración | Archivo | `Descripcion_CI.md` | `.md` | Raíz del repositorio | Documento de gestión |

## 🔁 Flujo de los trabajos prácticos

Cada `TP_<NN>_<Tema>/` conserva las siguientes entradas y salidas:

| Directorio | Contenido | Rol |
| --- | --- | --- |
| `00_Enunciado/` | Consigna, guía, aclaraciones y material provisto por la cátedra | Entrada |
| `01_Produccion/` | Artefactos de trabajo del grupo, incluyendo código fuente si corresponde | Trabajo en curso |
| `02_Entrega/` | Versión final presentada | Salida formal |
| `03_Retroalimentacion/` | Correcciones, calificaciones y devoluciones recibidas | Entrada posterior |
| `04_Evidencias_Repositorio/` | Capturas, reportes de Git, tags y pruebas de actualización | Evidencia de gestión |

Las carpetas se mantienen incluso cuando un TP no requiere contenido en alguna de ellas; así se preserva la consistencia entre entregas.

## Glosario

- `<NN>`: número de dos dígitos del TP, parcial o secuencia; por ejemplo, `04` o `05`.
- `<Tema>`: título corto del material; se utiliza `_` como separador de palabras.
- `<Artefacto>`: tipo de producto generado, por ejemplo `Resolucion`, `Informe`, `Checklist` o `Cronograma`.
- `<Descripcion>`: descripción breve de la evidencia, usando `_` como separador.
- `<AAAA-MM-DD>`: fecha en formato ISO 8601.
- `<ext>`: extensión permitida para el ítem de configuración.
- `v<MAJOR>.<MINOR>`: versión del archivo. `MAJOR` cambia ante una nueva entrega o modificación estructural relevante; `MINOR`, ante ajustes dentro de la misma entrega.
