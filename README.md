# IntelliDoc – Sistema Inteligente de Gestión y Análisis Documental

Proyecto Integrador – Desarrollo de Aplicaciones Empresariales (VI semestre)
Docente: Wilson Castaño Galviz — UTS

## Estructura del proyecto (entregables 1 a 13 del enunciado)

| Carpeta | Contenido | Estado |
|---|---|---|
| 01-Analisis | Documento de Análisis completo | ✅ Listo (v1.0) |
| 02-Diseno | Documento de Diseño completo (arquitectura, diagramas, modelo de datos) | ✅ Listo (v1.0) |
| 03-Desarrollo | Documento técnico | 🟡 Plantilla — se completa con el código |
| 04-Pruebas | Plan de pruebas y casos de prueba | 🟡 Plantilla con 15 casos de prueba iniciales |
| 05-Implementacion | Implementación y despliegue | 🟡 Plantilla |
| 06-Manual-Usuario | Manual de usuario | 🟡 Plantilla |
| 07-Manual-Tecnico | Manual técnico/administración | 🟡 Plantilla |
| 08-Matriz-Trazabilidad | Matriz de trazabilidad consolidada | 🟡 Plantilla inicial |
| 09-Codigo-Fuente | Código fuente | ✅ Backend y frontend presentes; repositorio Git remoto pendiente de verificar |
| 10-Base-Datos | Scripts de base de datos | ✅ Migración Alembic y script SQL documentado para MySQL |
| 11-Repositorio-Documentos-Prueba | Mínimo 30 documentos de prueba | ⬜ Lista y generador documentados; archivos físicos pendientes |
| 12-Video | Video de funcionamiento (máx. 5 min) | ⬜ Guion disponible; archivo de video pendiente |
| 13-Presentacion | Diapositivas de sustentación | 🟡 Estructura definida; archivo PPTX pendiente |

## Resumen del proyecto

Aplicación web que permite cargar documentos (PDF, DOCX, TXT), procesarlos automáticamente con IA (extracción de texto, clasificación, resumen, extracción de campos clave), buscar por contenido y hacer preguntas en lenguaje natural con respuestas basadas en los documentos reales (enfoque RAG), además de un dashboard de indicadores.

## Stack propuesto
- **Frontend:** React + Tailwind CSS
- **Backend:** Python + FastAPI
- **Base de datos:** MySQL 8.0
- **Base vectorial:** ChromaDB
- **Embeddings:** sentence-transformers (local)
- **LLM:** API de un proveedor configurable (clasificación, resumen, extracción, respuestas RAG)

Ver el detalle y la justificación completa en `02-Diseno/02-Documento-Diseno.md`.

---

## Estado actual y siguiente paso

El backend y el frontend ya están estructurados y cuentan con un flujo funcional base. La documentación debe mantenerse como una fotografía verificable del estado actual: no se deben marcar como ejecutados los casos que no tengan evidencia, y las limitaciones técnicas deben aparecer también en los manuales.

El primer bloque que sí se puede completar ya, sin escribir una sola línea de lógica de negocio, es:
1. **§1 Descripción del entorno de desarrollo** → registrar versiones reales de Python, Node.js, PostgreSQL, SO y editor que va a usar el equipo.
2. **§2 Configuración del proyecto** → crear la estructura de carpetas `backend/` y `frontend/`, inicializar el repositorio Git (entregable 09) y subir el primer commit con esta documentación.
3. **§3 Estructura del código fuente** → confirmar/ajustar el árbol de carpetas ya propuesto en el documento.

El siguiente paso prioritario es cerrar las brechas de validación: corregir la integración del almacén vectorial y el reprocesamiento, ejecutar la base de datos y la API, y capturar evidencias reales antes de afirmar que el sistema está completo.

---

## Parte 1 — Paso a paso para completar los documentos faltantes

| # | Documento | Qué necesita estar listo antes | Qué se hace en ese paso |
|---|---|---|---|
| 1 | **03-Desarrollo** | Nada (es el primero) | Documentar entorno, inicializar repo Git y estructura de carpetas (backend/frontend). Luego se va llenando sección por sección junto con el código (pasos 2 a 10 de la Parte 2). |
| 2 | **10-Base-Datos** | Modelos de datos definidos en el backend (paso 3 de la Parte 2) | Exportar el script SQL de creación de tablas (o migraciones) que reproduzca el modelo entidad-relación de 02-Diseño. |
| 3 | **11-Repositorio-Documentos-Prueba** | Nada — puede hacerse en paralelo con el código | Reunir/crear mínimo 30 documentos ficticios (PDF/DOCX/TXT) en al menos 3 categorías (ej. Contratos, Facturas, Informes), sin datos personales reales. |
| 4 | **04-Pruebas** | Sistema con las funcionalidades mínimas operativas (pasos 4 a 9 de la Parte 2) | Ejecutar los 15 casos de prueba ya redactados, registrar resultados reales, capturas y defectos encontrados. |
| 5 | **05-Implementacion** | Backend y frontend corriendo de extremo a extremo | Documentar instalación, variables de entorno reales (sin exponer claves), proceso de despliegue y evidencias del sistema funcionando. |
| 6 | **06-Manual-Usuario** | Frontend terminado | Redactar el paso a paso desde la perspectiva del usuario, con capturas de pantalla reales. |
| 7 | **07-Manual-Tecnico** | Instalación probada al menos una vez desde cero | Completar comandos reales, configuración de IA, problemas encontrados y su solución. |
| 8 | **08-Matriz-Trazabilidad** | Documentos 03 a 07 con contenido real | Consolidar la trazabilidad final: requisito → historia/caso de uso → componente de diseño → código → caso de prueba. |
| 9 | **12-Video** | Sistema funcional completo | Grabar demo de máx. 5 minutos cubriendo el guion de sustentación (sección 10 del enunciado). |
| 10 | **13-Presentacion** | Todo lo anterior cerrado | Armar las diapositivas de sustentación (requisitos, arquitectura, IA, pruebas, despliegue). |

---

## Parte 2 — Paso a paso para desarrollar el proyecto (código)

1. **Preparar entorno y repositorio Git** — crear repo remoto, estructura `backend/`/`frontend/`, `.gitignore`, `.env.example`. *(Alimenta 03-Desarrollo y 09-Codigo-Fuente.)*
2. **Backend base (FastAPI)** — proyecto mínimo corriendo (`/health`), configuración de variables de entorno y conexión a PostgreSQL.
3. **Modelo de datos y migraciones** — crear las tablas de 02-Diseño (usuarios, repositorios, documentos, fragmentos, logs_procesamiento, consultas_chat). *(Alimenta 10-Base-Datos.)*
4. **Autenticación y roles** — registro/login con JWT, roles Administrador/Usuario (RF-01, RF-02).
5. **Repositorios y carga de archivos** — CRUD de repositorios, subida/consulta/descarga/eliminación de PDF/DOCX/TXT con validaciones (RF-03, RF-04, RF-05).
6. **Extracción de texto** — integrar `pdfplumber` (PDF) y `python-docx` (DOCX) al pipeline (RF-06).
7. **Chunking + embeddings + ChromaDB** — dividir el texto, generar embeddings con `sentence-transformers` y guardarlos.
8. **Integración con el LLM (`AIService`)** — clasificación, resumen y extracción de campos clave (RF-07, RF-08, RF-09).
9. **Búsqueda por palabra clave y chat RAG** — endpoint de búsqueda y endpoint de preguntas en lenguaje natural con citación de fuentes (RF-10, RF-11).
10. **Dashboard y logs de errores** — indicadores del repositorio y registro/gestión de errores de procesamiento (RF-12, RF-13, RF-14).
11. **Frontend (React)** — pantallas de login, repositorios, detalle de documento, chat y dashboard, consumiendo la API anterior.
12. **Repositorio de documentos de prueba** — preparar los 30 documentos de prueba en paralelo a cualquiera de los pasos anteriores. *(Alimenta 11.)*
13. **Pruebas funcionales** — ejecutar y documentar los casos de prueba sobre el sistema ya integrado. *(Alimenta 04.)*
14. **Despliegue** — desplegar (local/VM) y documentar el proceso reproducible. *(Alimenta 05.)*
15. **Manuales** — redactar manual de usuario y manual técnico con el sistema ya funcionando. *(Alimenta 06 y 07.)*
16. **Cierre de trazabilidad, video y sustentación** — consolidar 08, grabar 12 y preparar 13.

---

## Próximos pasos sugeridos (resumen)
1. Ejecutar el bloque inmediato descrito arriba: entorno + repo Git + estructura de carpetas.
2. Avanzar el Paso 2 en adelante de la Parte 2 (backend base, modelo de datos, autenticación...).
3. Ir marcando cada documento de la Parte 1 como completado a medida que su prerrequisito quede listo.
