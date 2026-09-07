# 03 – Documento de Desarrollo / Documento Técnico
## Proyecto: IntelliDoc

**Estado:** 🟡 **Base implementada** — Existe un flujo funcional de autenticación, repositorios, documentos, procesamiento IA y frontend. La validación end-to-end sigue pendiente y hay limitaciones conocidas en RAG, reprocesamiento, permisos y evidencias.

## 1. Descripción del entorno de desarrollo
- **Sistema operativo:** Windows 11
- **Python:** 3.12.10
- **Node.js:** 22.20.0
- **npm:** 10.9.3
- **Editor/IDE:** VS Code
- **MySQL:** 8.0.x
- **Git:** 2.45.x

## 2. Configuración del proyecto
- Estructura de carpetas del repositorio (`backend/`, `frontend/`).
- Gestión de dependencias: `requirements.txt` (backend), `package.json` (frontend).
- Archivo `.env.example` con las variables necesarias (sin valores reales) en ambos proyectos. Los secretos no deben aparecer en el código ni en la documentación.
- `.gitignore` configurado para excluir `venv/`, `node_modules/`, `.env`, `__pycache__/`, `chroma_db/`, `dist/`, `coverage/`, archivos de IDE y SO.

## 3. Estructura del código fuente
```
09-Codigo-Fuente/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/        (auth, repositories, documents, chat, dashboard)
│   │   ├── services/       (auth_service, document_service, repository_service, processing_service, ai_service, search_service)
│   │   ├── models/         (modelos ORM)
│   │   ├── schemas/        (esquemas Pydantic)
│   │   └── core/           (config, seguridad, dependencias, database)
│   ├── alembic/            (migraciones de base de datos)
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
└── frontend/
    ├── src/
    │   ├── pages/          (Welcome, Login, Repositories, RepositoryDetail, DocumentDetail, Chat, Dashboard)
    │   ├── components/     (Layout)
    │   └── services/       (api.js - cliente Axios)
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── .env.example
    └── .gitignore
```

## 4. Implementación de frontend
- **Pantalla de bienvenida** (`Welcome.jsx`): Landing page con descripción del proyecto.
- **Pantalla Login** (`Login.jsx`): Formulario de autenticación con validación, manejo de errores y redirección.
- **Pantalla Repositorios** (`Repositories.jsx`): Lista con cards, modal para crear, estadísticas por estado/categoría, eliminar.
- **Pantalla Detalle Repositorio** (`RepositoryDetail.jsx`): Tabla de documentos con filtros por estado, modal upload (drag&drop), descargar, eliminar, ver detalle.
- **Pantalla Detalle Documento** (`DocumentDetail.jsx`): Metadatos, resumen IA, campos extraídos (JSON), logs de procesamiento, acciones (descargar, chat, reprocesar).
- **Pantalla Chat RAG** (`Chat.jsx`): Interfaz tipo chat, selector de repositorio, historial con fuentes citadas (similitud %), indicador de carga.
- **Pantalla Dashboard** (`Dashboard.jsx`): Métricas clave (cards), gráficos de barras (categoría/estado), tabla de errores recientes, pestaña logs completa.
- **Layout** (`Layout.jsx`): Sidebar responsive (mobile drawer), navegación por roles, avatar usuario, logout.
- **Ruteo protegido:** `ProtectedRoute` / `PublicRoute` con verificación de JWT en localStorage.
- **Cliente API** (`services/api.js`): Axios con interceptores para auth header y manejo 401.
- **Ruteo:** React Router v6 (`BrowserRouter` + `Routes` + `Outlet` para layout).
- **Estilos:** Tailwind CSS v3.4 con diseño responsivo, modo oscuro no implementado (fuera de alcance).
- **Proxy de desarrollo:** Vite proxy `/api` → `http://localhost:8000`.

## 5. Implementación de backend
- **FastAPI** 0.115.0 con Uvicorn 0.30.6.
- **Endpoint `/health`** (GET): responde `200 OK` con `{"status": "ok", "message": "IntelliDoc backend is running"}`.
- **Configuración centralizada** (`app/core/config.py`): `Settings` con `pydantic-settings`, carga desde `.env`, CORS para `http://localhost:5173` y `http://localhost:3000`.
- **Autenticación JWT** (`app/core/security.py`, `app/core/deps.py`): Hash bcrypt (`passlib`), tokens JWT HS256 (expiración 8 días), dependencias: `get_current_user`, `get_current_active_user`, `require_admin`.
- **Endpoints autenticación** (`app/routers/auth.py`): `POST /auth/login`, `POST /auth/register` (admin), `GET/PUT /auth/me`, CRUD usuarios (admin).
- **CRUD Repositorios** (`app/routers/repositories.py`): `POST/GET/PUT/DELETE /repositories` con autorización propietario/admin, endpoint `/repositories/{id}` con estadísticas.
- **CRUD Documentos** (`app/routers/documents.py`): `POST /documents` (multipart, validación tipo/tamaño), `GET /documents` (filtros), `GET /documents/search?q=` (keyword), `GET /documents/{id}/download`, `PUT/DELETE` con permisos.
- **Chat RAG** (`app/routers/chat.py`): `POST /chat` (pregunta + repo opcional → respuesta + fuentes), `GET /chat/history`.
- **Dashboard** (`app/routers/dashboard.py`): `GET /dashboard/summary` (métricas + errores), `GET /dashboard/logs`, `POST /dashboard/documents/{id}/reprocess`.
- **Dependencias:** `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `python-jose`, `passlib[bcrypt]`, `sqlalchemy`, `psycopg2-binary`, `alembic`, `pdfplumber`, `python-docx`, `sentence-transformers`, `chromadb`, `httpx`, `python-dotenv`, `email-validator`, `aiofiles`, `google-generativeai`, `numpy<2.0`, `scipy<1.18`.

## 6. Implementación de base de datos y almacenamiento
- **Modelos SQLAlchemy** (`app/models/`): Usuario, Repositorio, Documento, Fragmento, LogProcesamiento, ConsultaChat — siguiendo modelo E-R de 02-Diseño.
- **Migraciones Alembic** (`alembic/`): Migración `7a8fb6f3c4e7` crea 6 tablas con PK, FK (CASCADE), índices, constraints, JSONB para campos variables.
- **Base de datos:** MySQL (`DATABASE_URL` en `.env`).
- **Almacenamiento archivos:** Carpeta local `storage/` (sanitización de nombres), referenciada en BD.

## 7. Implementación del procesamiento de documentos (Pipeline IA)
**Servicio:** `app/services/processing_service.py` — `ProcessingService`

| Etapa | Descripción | Tecnología |
|-------|-------------|------------|
| 1. Extracción texto | PDF (pdfplumber), DOCX (python-docx), TXT (lectura directa) | `pdfplumber`, `python-docx` |
| 2. Chunking | División ~500 tokens con solapamiento 50 | Algoritmo propio por palabras |
| 3. Embeddings | Vectorización semántica | `sentence-transformers` (`all-MiniLM-L6-v2`) local |
| 4. Almacenamiento vectores | ChromaDB persistente local | `chromadb.PersistentClient` (cosine space) |
| 5. Almacenamiento fragmentos | MySQL tabla `fragmentos` (texto + vector_id + orden) | SQLAlchemy |

**Flujo actual:** Al subir documento → estado `pendiente` → procesamiento síncrono dentro de la solicitud → `procesando` → pipeline → `procesado`/`error` + logs en `logs_procesamiento`. No hay una cola persistente ni un `BackgroundTask` activo.

## 8. Integración de IA (Gemini API)
**Servicio:** `app/services/ai_service.py` — `AIService` (abstracción proveedor)

- **Proveedor:** Google Gemini (`google-generativeai`), modelo `gemini-1.5-flash` (configurable via `LLM_MODEL`).
- **API Key:** Variable `LLM_API_KEY` en `.env` (nunca hardcodeada).
- **Prompts estructurados** para cada tarea:

| Método | Prompt | Salida |
|--------|--------|--------|
| `clasificar(texto)` | Categorías cerradas: Contrato, Factura, Informe, Otro | Categoría única |
| `resumir(texto)` | Resumen conciso 3 párrafos, info clave | Texto libre |
| `extraer_campos(texto, categoría)` | JSON schema según tipo (factura/contrato/informe) | JSON validado |
| `responder_pregunta(pregunta, fragmentos)` | RAG: contexto + cita fuentes, no inventar | Respuesta + fuentes |

## 9. Implementación de clasificación, resumen y extracción (RF-07, RF-08, RF-09)
**Integración:** Al finalizar pipeline exitoso, `ProcessingService` llama a `AIService`:
1. `categoria = ai_service.clasificar(texto_completo)`
2. `resumen = ai_service.resumir(texto_completo)`
3. `campos = ai_service.extraer_campos(texto_completo, categoria)`
4. Actualiza `Documento` con resultados y estado `procesado`.

**Validación:** JSON parseado con fallback a raw text si falla. Categorías validadas contra lista permitida.

## 10. Implementación de búsqueda y consulta documental (RF-10, RF-11)
| Tipo | Endpoint | Implementación |
|------|----------|----------------|
| Palabra clave | `GET /documents/search?q=` | `DocumentService.search_documentos()` — ILIKE en resumen, nombre, campos_extraidos |
| Semántica (RAG) | `POST /chat` | `SearchService.chat()` → embedding pregunta → ChromaDB top-k → `AIService.responder_pregunta()` → guarda en `consultas_chat` |

**Citación de fuentes:** La respuesta está diseñada para incluir `documento_id`, `nombre_archivo`, `fragmento_texto` y `similitud` (0-1). Debe verificarse con una instancia compartida y persistente de ChromaDB; actualmente `ProcessingService` y `SearchService` crean clientes efímeros separados.

**Regla RN-06:** Si no hay fragmentos relevantes → "No encontré información suficiente en los documentos para responder a esta pregunta."

## 11. Dashboard y logs (RF-12, RF-13, RF-14)
**Endpoints:**
- `GET /dashboard/summary` → `DashboardStats`: totales, por categoría, por estado, últimos 10 errores.
- `GET /dashboard/logs` → Lista paginada `LogProcesamientoResumen` (filtro repositorio/tipo).
- `POST /dashboard/documents/{id}/reprocess` → Re-ejecuta pipeline completo + IA.

**Frontend:** Cards métricas, gráficos SVG simples (barras), tabla errores con tipo/fecha, pestaña logs completa con tabla.

## 12. Gestión de errores y validaciones
- **Archivos:** Validación backend (extensión + tamaño 10MB) en `upload_documento` antes de guardar.
- **Path traversal:** Nombres sanitizados (`{user_id}_{repo_id}_{filename}`).
- **Excepciones HTTP:** 400 (validación), 401 (auth), 403 (permisos), 404 (no existe), 500 (servidor).
- **Logs:** Tabla `logs_procesamiento` registra cada etapa (info/error) con timestamp.
- **Reprocesamiento:** Está documentado como objetivo, pero requiere corrección: la ruta actual invoca un método inexistente en `ProcessingService` y mezcla `PersistentClient` con la indexación efímera.

## 13. Seguridad de credenciales y variables de entorno
- `.env.example` en `backend/` y `frontend/` con placeholders.
- `.gitignore` excluye `.env`, `.env.*`, `venv/`, `node_modules/`, `chroma_db/`, `__pycache__/`.
- `SECRET_KEY` (JWT), `LLM_API_KEY` (Gemini), `DATABASE_URL` solo por variable de entorno.
- Contraseñas: `bcrypt` hash (nunca texto plano).
- JWT: HS256, expiración 8 días (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- CORS: Orígenes explícitos en `BACKEND_CORS_ORIGINS`.

## 14. Control de versiones mediante Git
- El código está organizado en `09-Codigo-Fuente/`. La existencia de un repositorio Git remoto y de commits reproducibles debe verificarse antes de entregar.
- Convención: `main` / `feature/*` + commits convencionales (`feat:`, `fix:`, `chore:`, `docs:`).

## 15. Registro de avances / bitácora de desarrollo
| Fecha | Avance | Responsable |
|---|---|---|
| 2025-09-06 | Estructura docs inicial, carpetas backend/frontend, FastAPI `/health`, React+Vite+Tailwind Welcome | IA + Hansel |
| 2025-09-06 | Modelos SQLAlchemy (6 tablas), migración Alembic, JWT auth, CRUD repos/documentos, validación archivos | IA + Hansel |
| 2025-09-06 | Pipeline IA (extracción→chunking→embeddings→ChromaDB), AIService Gemini, RAG chat, Dashboard, reprocesamiento | IA + Hansel |
| 2025-09-06 | Frontend completo: Login, Repositorios, DocumentDetail, Chat, Dashboard, Layout, routing protegido | IA + Hansel |

## 16. Manual técnico de instalación y ejecución
### Backend
```bash
cd 09-Codigo-Fuente/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env:
# DATABASE_URL=mysql+pymysql://usuario:clave@localhost:3306/intellidoc
# SECRET_KEY=clave-secreta-32-chars-minimo
# LLM_API_KEY=tu-gemini-api-key
# LLM_MODEL=gemini-1.5-flash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
→ API: `http://localhost:8000` | Docs: `http://localhost:8000/docs`

### Frontend
```bash
cd 09-Codigo-Fuente/frontend
npm install
cp .env.example .env
# VITE_API_URL=http://localhost:8000/api/v1
npm run dev
```
→ UI: `http://localhost:5173` (proxy `/api` → backend)

### Pruebas rápidas
```bash
# 1. Crear admin
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Admin","correo":"admin@local","password":"<clave_local>","rol":"administrador"}'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"admin@local","password":"<clave_local>"}'
# → Copiar access_token

# 3. Crear repositorio
curl -X POST http://localhost:8000/api/v1/repositories \
  -H "Authorization: Bearer TU_TOKEN" -H "Content-Type: application/json" \
  -d '{"nombre":"Mis Documentos"}'

# 4. Subir PDF
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Authorization: Bearer TU_TOKEN" \
  -F "repositorio_id=REPO_ID" -F "file=@documento.pdf"

# 5. Preguntar (RAG)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer TU_TOKEN" -H "Content-Type: application/json" \
  -d '{"pregunta":"¿Cuál es el total de la factura?","repositorio_id":"REPO_ID"}'
```