# 09 – Código Fuente

Repositorio local del proyecto IntelliDoc con estructura `backend/` y `frontend/`.

## Estado
✅ **PROYECTO COMPLETAMENTE FUNCIONAL** — Todos los requerimientos implementados y probados.

### Backend (FastAPI + Python)
- ✅ Autenticación JWT (login, registro, roles admin/usuario)
- ✅ CRUD Repositorios y Documentos (validación backend tipo/tamaño)
- ✅ Pipeline IA completo: extracción → chunking → embeddings → ChromaDB
- ✅ AIService con Gemini API (clasificación, resumen, extracción campos)
- ✅ Chat RAG (`POST /chat`) con citación de fuentes
- ✅ Dashboard con métricas, gráficos y logs
- ✅ Reprocesamiento de documentos en error
- ✅ Modelos SQLAlchemy (6 tablas) + Migración Alembic

### Frontend (React + Vite + Tailwind)
- ✅ Login con validación y manejo de errores
- ✅ Repositorios: lista, crear, estadísticas, eliminar
- ✅ Detalle Repositorio: tabla documentos, filtros, upload modal, acciones
- ✅ Detalle Documento: metadatos, resumen IA, campos JSON, logs, descargar
- ✅ Chat RAG: selector repositorio, historial, fuentes con similitud %
- ✅ Dashboard: cards métricas, gráficos barras, tabla errores, tabs
- ✅ Layout responsive con sidebar, navegación por roles, logout

## Estructura completa
```
09-Codigo-Fuente/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── repositories.py
│   │   │   ├── documents.py
│   │   │   ├── chat.py
│   │   │   └── dashboard.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── document_service.py
│   │   │   ├── repository_service.py
│   │   │   ├── processing_service.py
│   │   │   ├── ai_service.py
│   │   │   └── search_service.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── usuario.py
│   │   │   ├── repositorio.py
│   │   │   ├── documento.py
│   │   │   ├── fragmento.py
│   │   │   ├── log_procesamiento.py
│   │   │   └── consulta_chat.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── usuario.py
│   │   │   ├── repositorio.py
│   │   │   ├── documento.py
│   │   │   ├── chat.py
│   │   │   └── dashboard.py
│   │   └── core/
│   │       ├── config.py
│   │       ├── database.py
│   │       ├── security.py
│   │       └── deps.py
│   ├── alembic/
│   │   ├── env.py
│   │   ├── versions/
│   │   │   └── 7a8fb6f3c4e7_initial_migration_crear_tablas_usuarios_.py
│   │   └── script.py.mako
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── pages/
│   │   │   ├── Welcome.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Repositories.jsx
│   │   │   ├── RepositoryDetail.jsx
│   │   │   ├── DocumentDetail.jsx
│   │   │   ├── Chat.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── components/
│   │   │   └── Layout.jsx
│   │   └── services/
│   │       └── api.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   └── .gitignore
```

## Endpoints implementados (API v1 - `/api/v1`)

### Autenticación (`/auth`)
- `POST /auth/login` — Login, retorna JWT
- `POST /auth/register` — Registrar usuario (solo admin)
- `GET /auth/me` — Usuario actual
- `PUT /auth/me` — Actualizar perfil
- `GET /auth/users` — Listar usuarios (admin)
- `POST /auth/users` — Crear usuario (admin)
- `GET /auth/users/{id}` — Obtener usuario (admin)
- `PUT /auth/users/{id}` — Actualizar usuario (admin)
- `DELETE /auth/users/{id}` — Eliminar usuario (admin)

### Repositorios (`/repositories`)
- `POST /repositories` — Crear repositorio
- `GET /repositories` — Listar (propios o todos si admin)
- `GET /repositories/{id}` — Detalle con estadísticas
- `PUT /repositories/{id}` — Actualizar
- `DELETE /repositories/{id}` — Eliminar

### Documentos (`/documents`)
- `POST /documents` — Subir archivo (multipart, validación tipo/tamaño)
- `GET /documents` — Listar (filtros: repositorio_id, estado)
- `GET /documents/search?q=` — Búsqueda por palabra clave (RF-10)
- `GET /documents/{id}` — Detalle completo (metadatos, resumen, campos)
- `GET /documents/{id}/download` — Descargar archivo original
- `PUT /documents/{id}` — Actualizar metadatos
- `DELETE /documents/{id}` — Eliminar (borra archivo físico + vectores)

### Chat RAG (`/chat`) — **RF-11**
- `POST /chat` — Pregunta en lenguaje natural → respuesta + fuentes citadas
- `GET /chat/history` — Historial de consultas del usuario

### Dashboard (`/dashboard`) — **RF-12, RF-13, RF-14**
- `GET /dashboard/summary` — Métricas: totales, por categoría, por estado, últimos errores
- `GET /dashboard/logs` — Logs de procesamiento (filtro repositorio/tipo)
- `POST /dashboard/documents/{id}/reprocess` — Reprocesar documento en error

## Cómo ejecutar

### Prerrequisitos
- MySQL 8.0+ corriendo en `localhost:3306`
- Base de datos `intellidoc` creada
- API Key de Gemini (gratis en https://makersuite.google.com/app/apikey)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con valores reales:
# DATABASE_URL=mysql+pymysql://usuario:clave@localhost:3306/intellidoc
# SECRET_KEY=clave-secreta-de-almenos-32-caracteres
# LLM_API_KEY=tu-gemini-api-key
# LLM_MODEL=gemini-1.5-flash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
→ API: `http://localhost:8000` | Docs Swagger: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# VITE_API_URL=http://localhost:8000/api/v1
npm run dev
```
→ UI: `http://localhost:5173` (proxy `/api` → `http://localhost:8000`)

## Flujo completo de prueba
```bash
# 1. Crear usuario admin
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Admin","correo":"admin@local","password":"<clave_local>","rol":"administrador"}'

# 2. Login → obtener access_token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"admin@local","password":"<clave_local>"}'

# 3. Crear repositorio
curl -X POST http://localhost:8000/api/v1/repositories \
  -H "Authorization: Bearer TU_TOKEN" -H "Content-Type: application/json" \
  -d '{"nombre":"Contratos 2024"}'

# 4. Subir documento (PDF/DOCX/TXT)
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Authorization: Bearer TU_TOKEN" \
  -F "repositorio_id=ID_REPO" -F "file=@contrato.pdf"

# 5. Esperar procesamiento (estado → "procesado")
# Ver en frontend o: curl -H "Authorization: Bearer TU_TOKEN" http://localhost:8000/api/v1/documents/ID_DOC

# 6. Preguntar en lenguaje natural (RAG)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer TU_TOKEN" -H "Content-Type: application/json" \
  -d '{"pregunta":"¿Cuál es el valor total del contrato?","repositorio_id":"ID_REPO"}'
# → Respuesta con fuentes: [{"documento_id": "...", "nombre_archivo": "contrato.pdf", "similitud": 0.89}]

# 7. Ver dashboard
curl -H "Authorization: Bearer TU_TOKEN" http://localhost:8000/api/v1/dashboard/summary
```

## Requerimientos funcionales cubiertos (100%)
| RF | Descripción | Implementación |
|---|---|---|
| RF-01 | Autenticación JWT | `app/routers/auth.py`, `app/core/security.py` |
| RF-02 | Roles Administrador/Usuario | `app/core/deps.py:require_admin` |
| RF-03 | CRUD Repositorios | `app/routers/repositories.py` |
| RF-04 | Cargar archivos (PDF/DOCX/TXT) | `app/routers/documents.py:upload_documento` |
| RF-05 | Consultar/Descargar/Eliminar | `app/routers/documents.py` |
| RF-06 | Extracción automática texto | `app/services/processing_service.py:extract_text` |
| RF-07 | Clasificación (3+ categorías) | `app/services/ai_service.py:clasificar` (Gemini) |
| RF-08 | Resumen automático | `app/services/ai_service.py:resumir` (Gemini) |
| RF-09 | Extracción campos (3 tipos) | `app/services/ai_service.py:extraer_campos` (Gemini + JSON) |
| RF-10 | Búsqueda palabra clave | `app/routers/documents.py:search_documentos` |
| RF-11 | Preguntas lenguaje natural (RAG) | `app/routers/chat.py`, `app/services/search_service.py` |
| RF-12 | Dashboard indicadores | `app/routers/dashboard.py:dashboard_summary` |
| RF-13 | Estados procesamiento | `app/models/documento.py:estado` + pipeline |
| RF-14 | Logs errores + reprocesar | `app/routers/dashboard.py:reprocesar_documento` |

## Próximos pasos (fuera de alcance actual)
1. Despliegue en producción (Docker, Nginx, HTTPS)
2. Tests automatizados (pytest + Playwright)
3. OCR para PDFs escaneados
4. Multi-tenant / organizaciones
5. Notificaciones email/webhook