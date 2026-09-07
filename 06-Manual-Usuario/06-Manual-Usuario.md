# 06 – Manual de Usuario
## Proyecto: IntelliDoc – Sistema Inteligente de Gestión y Análisis Documental

**Versión:** 1.1 | **Estado:** guía del flujo base; funciones pendientes identificadas en el texto

---

## 1. Introducción

**IntelliDoc** es una aplicación web que transforma repositorios de documentos pasivos (PDF, DOCX, TXT) en una base de conocimiento inteligente. Permite:

- **Clasificar** automáticamente documentos (Contrato, Factura, Informe, Otro)
- **Resumir** contenido en 3 párrafos clave
- **Extraer** datos estructurados (fechas, montos, partes, etc.)
- **Buscar** por palabras clave en el contenido real
- **Preguntar** en lenguaje natural y recibir respuestas basadas **solo** en tus documentos (RAG)
- **Visualizar** indicadores y métricas en un Dashboard

---

## 2. Primer acceso y autenticación

### 2.1 URL de acceso
```
http://localhost:5173
```
*(En producción: URL proporcionada por administrador)*

### 2.2 Pantalla de Login

![Login](evidencias/login_page.png)

**Campos:**
- **Correo electrónico:** Tu usuario registrado
- **Contraseña:** Tu contraseña

**Botones:**
- **Iniciar sesión** → Accede al sistema
- **Crear cuenta gratis** → Registro de nuevo usuario (primer usuario = Administrador)

### 2.3 Acceso de prueba (solo entorno local)
| Rol | Correo | Contraseña |
|---|---|---|
Las credenciales deben crearse localmente. Este manual no publica contraseñas.

### 2.4 Recuperación de contraseña
> **Nota:** En esta versión no hay recuperación automática. Contacta al administrador para resetear contraseña.

---

## 3. Navegación principal (Sidebar)

Al iniciar sesión, verás el menú lateral izquierdo:

| Icono | Opción | Descripción | Disponible para |
|---|---|---|---|
| 📁 | **Repositorios** | Gestión de carpetas y documentos | Todos |
| 💬 | **Chat** | Preguntas en lenguaje natural (RAG) | Todos |
| 📊 | **Dashboard** | Métricas, gráficos, logs de error | Administrador |
| ⚙️ | **Administración** | Usuarios, logs globales | Administrador |

**Perfil de usuario** (esquina inferior izquierda): Muestra tu nombre, rol y botón **Cerrar sesión**.

---

## 4. Gestión de Repositorios

### 4.1 Lista de repositorios
Al entrar verás tarjetas (cards) por cada repositorio:

![Repositorios](evidencias/repositories_list.png)

**Información visible por tarjeta:**
- **Nombre** del repositorio
- **Total de documentos** (badge numérico)
- **Distribución por estado** (badges de color):
  - 🟢 **Procesado** (verde)
  - 🔵 **Procesando** (azul)
  - ⚪ **Pendiente** (gris)
  - 🔴 **Error** (rojo)
- **Distribución por categoría** (badges índigo): Contrato, Factura, Informe, Otro

**Acciones:**
- **Clic en tarjeta** → Ver detalle del repositorio
- **Botón "Nuevo Repositorio"** (arriba derecha) → Modal crear
- **Botón 🗑️** (hover tarjeta) → Eliminar (confirma)

### 4.2 Crear repositorio
1. Click **"Nuevo Repositorio"**
2. Ingresar **Nombre** (ej: "Contratos 2024", "Facturas Proveedores")
3. Click **"Crear"**
4. El repositorio aparece en la lista automáticamente

### 4.3 Eliminar repositorio
1. Hover sobre tarjeta → Click 🗑️
2. Confirmar: *"¿Eliminar este repositorio y todos sus documentos?"*
3. **¡Atención!** Se eliminan **todos** los documentos, fragmentos, vectores y logs asociados.

---

## 5. Gestión de Documentos

### 5.1 Vista detalle de repositorio
Al entrar a un repositorio verás una tabla con todos los documentos:

![Repo Detail](evidencias/repo_detail_upload.png)

**Columnas:**
| Columna | Descripción |
|---|---|
| **Documento** | Nombre archivo (link a detalle) |
| **Formato** | Badge: PDF / DOCX / TXT |
| **Estado** | Badge color: Pendiente/Procesando/Procesado/Error |
| **Categoría** | Asignada por IA (tras procesar) |
| **Acciones** | Ver 👁️ | Descargar ⬇️ | Eliminar 🗑️ |

**Filtros disponibles:**
- **Filtro por estado** (dropdown): Todos / Pendiente / Procesando / Procesado / Error

### 5.2 Subir documento
1. Click botón **"Subir documento"** (arriba derecha)
2. **Modal de carga:**
   - **Repositorio:** Pre-seleccionado (o elige de dropdown)
   - **Archivo:** Click o drag & drop (PDF, DOCX, TXT máx 10MB)
2. Click **"Subir"**
3. **Resultado:** Documento aparece en tabla con estado **"Pendiente"**
4. **Procesamiento automático:** En 2-5 segundos cambia a **"Procesando"** → **"Procesado"** (o **"Error"**)

![Upload Modal](evidencias/repo_detail_upload.png)

**Validaciones automáticas:**
- ✅ Formato: PDF, DOCX, TXT
- ✅ Tamaño: ≤ 10 MB
- ✅ Nombre sanitizado (evita `../../../etc/passwd`)

### 5.3 Detalle de documento
Click en nombre del documento → Vista completa:

![Detalle IA](evidencias/doc_detail_ia.png)

**Secciones:**
1. **Información general:** Nombre, formato, fechas, repositorio, estado
2. **Categoría IA:** Badge color (Contrato=Azul, Factura=Verde, Informe=Naranja, Otro=Gris)
3. **Resumen IA:** 3 párrafos máx. generados por Gemini
4. **Campos extraídos (JSON):** Estructura según tipo:
   - **Factura:** número, fecha, proveedor, cliente, total, impuestos, moneda
   - **Contrato:** número, fechas inicio/fin, partes, objeto, valor, moneda
   - **Informe:** título, autor, fecha, tema, conclusiones[], recomendaciones[]
4. **Logs de procesamiento:** Tabla cronológica (tipo, mensaje, fecha)
5. **Acciones:** Descargar ⬇️ | Chat 💬 | Reprocesar 🔄 (solo Admin si error)

### 5.4 Descargar documento
1. En tabla o detalle → Botón **Descargar ⬇️**
2. Se descarga archivo original con nombre original

### 5.5 Eliminar documento
1. Click 🗑️ → Confirmar
2. Se elimina: archivo físico + registro BD + fragmentos ChromaDB + logs

---

## 6. Búsqueda de documentos

### 6.1 Búsqueda por palabra clave

> Estado actual: el backend dispone de un endpoint de búsqueda, pero la búsqueda sobre el texto completo y su integración visual aún requieren validación. No presentar esta función como completamente disponible hasta comprobarla en la aplicación.
En vista de repositorio → Campo **"Buscar..."** (arriba derecha de tabla)

**Busca en:** Contenido extraído, nombre archivo, campos extraídos, resumen

**Ejemplos:**
| Búsqueda | Encuentra |
|---|---|
| `"arrendamiento"` | Contratos con esa palabra en texto |
| `"factura_001"` | Archivo exacto por nombre |
| `"500 USD"` | Documentos con ese monto en campos/resumen |

**Resultados:** Tabla filtrada + badge "X resultados"

---

## 7. Chat Inteligente (RAG)

### 7.1 Acceso
Menú lateral → **Chat** 💬

### 7.2 Interfaz

![Chat](evidencias/chat_rag_sources.png)

**Componentes:**
1. **Selector de repositorio** (arriba): Limita búsqueda a un repositorio
2. **Historial de chat:** Burbujas usuario (azul, derecha) / IA (gris, izquierda)
3. **Fuentes citadas:** Cada respuesta IA muestra badges `[1] [2] [3]` con:
   - Nombre archivo
   - % Similitud semántica (0-100%)
   - Click → Abre detalle documento
4. **Input inferior:** Escribe pregunta + Enter/Enviar

### 7.3 Hacer una pregunta
1. Selecciona repositorio (opcional: "Todos")
2. Escribe pregunta natural:
   - ✅ *"¿Cuál es el total de la factura 001?"*
   - ✅ *"¿Qué contratos vencen en diciembre?"*
   - ✅ *"¿Quiénes son las partes del contrato de arrendamiento?"*
   - ❌ *"¿Cómo está el clima?"* (fuera de contexto)
2. Presiona **Enter** o botón **Enviar**
3. **Indicador:** "Pensando..." → Respuesta + fuentes

### 7.4 Entender la respuesta
- **Respuesta:** Texto generado por Gemini **basado solo en tus documentos**
- **Fuentes `[1] [2] [3]`:** Click para ver fragmento exacto + % similitud
- **Sin info:** *"No encontré información suficiente en los documentos para responder a esta pregunta."*

### 7.5 Historial
- Se guarda automáticamente (pregunta, respuesta, fuentes, fecha)
- Accesible en misma pestaña (scroll arriba)
- Persistente entre sesiones (mismo usuario)

---

## 8. Dashboard (Solo Administrador)

### 8.1 Acceso
Menú lateral → **Dashboard** 📊

### 8.2 Pestaña "Resumen"

![Dashboard](evidencias/dashboard_metrics.png)

**Tarjetas métricas (cards):**
| Métrica | Descripción |
|---|---|
| **Total repositorios** | Cantidad total en sistema |
| **Total documentos** | Suma global |
| **Usuarios** | Total usuarios registrados |
| **Errores recientes** | Docs en estado error (últimos 10) |

**Gráficos de barras SVG:**
- **Documentos por categoría:** Barras horizontales (Contrato, Factura, Informe, Otro)
- **Documentos por estado:** Barras (Procesado, Pendiente, Procesando, Error)

**Tabla "Errores recientes":** Últimos 10 logs tipo error con:
- Nombre archivo | Tipo error | Mensaje | Fecha

### 8.3 Pestaña "Logs"
Tabla completa paginada de `logs_procesamiento`:
- Filtros: Repositorio, Tipo error
- Columnas: Documento, Tipo, Mensaje, Fecha
- Paginación: 20 por página

### 8.4 Reprocesar documento en error
1. En pestaña Logs o Dashboard → Documento con error
2. Botón **"Reprocesar" 🔄**
3. Flujo: `Error` → `Pendiente` → `Procesando` → `Procesado` (o `Error` si persiste)

---

## 9. Administración de Usuarios (Solo Admin)

> Estado actual: existen endpoints backend para usuarios, pero la ruta y pantalla de administración no están registradas en el frontend.

### 9.1 Acceso
Menú lateral → **Administración** → **Usuarios**

### 9.2 Lista usuarios
Tabla con: Nombre, Correo, Rol, Activo, Acciones (Editar/Eliminar)

### 9.3 Crear usuario
1. Botón **"Nuevo usuario"**
2. Formulario: Nombre, Correo, Contraseña (mín 8 chars), Rol (Admin/Usuario)
3. **Primer usuario creado = Administrador automáticamente**

### 9.4 Editar/Desactivar
- **Editar:** Cambiar nombre, correo, rol, estado activo/inactivo
- **Eliminar:** Solo Admin, no puede eliminarse a sí mismo

---

## 10. Preguntas frecuentes (FAQ)

| Pregunta | Respuesta |
|---|---|
| **¿Puedo subir imágenes (JPG/PNG)?** | No. Solo PDF, DOCX, TXT en esta versión. |
| **¿Funciona con PDFs escaneados (sin texto)?** | No. Requiere OCR (fuera de alcance v1.0). Usa PDFs con texto seleccionable. |
| **¿Se pierden los vectores al reiniciar?** | Sí. La implementación usa ChromaDB efímero y los servicios de procesamiento y chat crean clientes separados. La solución prevista es usar un cliente persistente y compartido. |
| **¿Cuántos docs soporta?** | Probado hasta 100 docs sin degradación. Para miles: ChromaDB Persistent + BD dedicada. |
| **¿Puedo usar otro LLM (OpenAI, Anthropic)?** | Sí, cambia `LLM_PROVIDER` y `LLM_API_KEY` en `.env`; adapta `AIService._call_llm()`. |
| **¿Cómo cambio la cuota Gemini?** | En [Google AI Studio](https://ai.google.dev/) → "Get API key" → Upgrade plan. |
| **¿Puedo corregir la categoría que puso la IA?** | Solo Admin: edita documento → cambia categoría → guarda. Queda registrado en logs. |
| **¿Por qué mi documento queda en "Error"?** | Revisa logs: causas comunes = API key inválida, cuota agotada, PDF corrupto, LLM timeout. |

---

## 11. Atajos de teclado

| Acción | Atajo |
|---|---|
| Enviar pregunta en Chat | `Enter` |
| Nueva línea en Chat | `Shift + Enter` |
| Cerrar modal | `Escape` |
| Foco en búsqueda | `/` (en vista repositorio) |

---

## 12. Soporte y contacto

| Problema | Contacto |
|---|---|
| Error técnico / Bug | admin@intelldoc.local |
| Solicitud funcionalidad | Jira/Backlog del proyecto |
| Acceso / Credenciales | Administrador del sistema |

---

**IntelliDoc v1.0** — *Transforma tus documentos en conocimiento accionable*

*Manual actualizado para reflejar el estado verificable del workspace. Las capturas y funciones pendientes deben agregarse después de una ejecución real.*