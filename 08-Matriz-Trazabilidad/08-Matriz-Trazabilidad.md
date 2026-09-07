# 08 – Matriz de Trazabilidad de Requisitos, Funcionalidades y Pruebas
## Proyecto: IntelliDoc

**Estado:** 🟡 **Matriz base** — Los requisitos están relacionados con diseño, código y casos de prueba documentados. La trazabilidad no se considera cerrada hasta corregir las rutas, validar los casos y adjuntar evidencias reales.

### Criterio de estado

- **Implementado:** existe código identificable, aunque aún puede requerir prueba de integración.
- **Parcial:** existe una parte del flujo, pero no cumple completamente el requisito o tiene una limitación conocida.
- **Pendiente de evidencia:** el caso está diseñado o declarado, pero no hay evidencia física reproducible en el workspace.

| Requisito | Historia de usuario | Caso de uso | Componente de diseño | Implementación (código) | Caso(s) de prueba |
|---|---|---|---|---|---|
| RF-01 | — | CU-01 (Login) | Módulo Auth / AuthService | `app/routers/auth.py:login`, `app/services/auth_service.py:authenticate`, `app/core/security.py:verify_password` | CP-01 (Login exitoso), CP-02 (Login fallido), CP-03 (Token inválido) |
| RF-02 | — | CU-01 (Roles) | Módulo Auth (roles) | `app/core/deps.py:require_admin`, `app/models/usuario.py:rol`, `app/routers/auth.py:register` | CP-03 (Acceso admin), CP-04 (Acceso denegado usuario normal) |
| RF-03 | HU-01 | CU-02 (CRUD Repositorios) | RepositoryService | `app/routers/repositories.py` (POST/GET/PUT/DELETE), `app/services/repository_service.py` | CP-05 (Crear repo), CP-06 (Listar), CP-07 (Actualizar), CP-08 (Eliminar) |
| RF-04 | HU-01 | CU-03 (Subir archivo) | DocumentService / Router Documents | `app/routers/documents.py:upload_documento`, `app/services/document_service.py:create_documento`, validación `validate_file` | CP-09 (Subida PDF), CP-10 (Subida DOCX), CP-11 (Subida TXT), CP-12 (Rechazar tipo inválido), CP-13 (Rechazar tamaño >10MB) |
| RF-05 | HU-01 | CU-04 (Consultar/Descargar/Eliminar) | DocumentService | `app/routers/documents.py` (GET, GET download, DELETE), `app/services/document_service.py` | CP-14 (Descargar), CP-15 (Eliminar), CP-16 (Listar con filtros) |
| RF-06 | HU-01 | CU-05 (Extracción texto) | ProcessingPipeline | `app/services/processing_service.py:extract_text` (pdfplumber/python-docx/TXT) | CP-17 (Extraer texto PDF/DOCX/TXT) |
| RF-07 | — | CU-05 (Clasificación) | AIService.clasificar | `app/services/ai_service.py:clasificar` (Gemini + prompt categorías) | CP-18 (Clasificar 3+ categorías) |
| RF-08 | HU-02 | CU-05 (Resumen) | AIService.resumir | `app/services/ai_service.py:resumir` (Gemini + prompt resumen) | CP-19 (Generar resumen automático) |
| RF-09 | — | CU-05 (Extracción campos) | AIService.extraer_campos | `app/services/ai_service.py:extraer_campos` (Gemini + JSON schema por tipo) | CP-20 (Extraer campos 3 tipos doc) |
| RF-10 | HU-03 | CU-06 (Búsqueda keyword) | SearchService (keyword) | `app/services/document_service.py:search_documentos`, `app/routers/documents.py:search_documentos` | CP-21 (Búsqueda contenido), CP-22 (Búsqueda nombre) | Parcial: no busca texto completo ni hay evidencia física |
| RF-11 | HU-04 | CU-08 (Chat RAG) | SearchService (RAG) + AIService | `app/services/search_service.py:chat` (embeddings + ChromaDB + Gemini), `app/routers/chat.py` | CP-23 (RAG respuesta + fuentes), CP-24 (RAG sin info → "no encontré") | Parcial: ChromaDB efímero y clientes separados |
| RF-12 | HU-05 | CU-09 (Dashboard) | DashboardService | `app/routers/dashboard.py:dashboard_summary` (métricas, gráficos, errores), `frontend/src/pages/Dashboard.jsx` | CP-25 (Dashboard indicadores) | Parcial: falta exigir rol admin y evidencia |
| RF-13 | — | CU-05 (Estados) | DocumentService (estado) | `app/models/documento.py:estado`, `app/services/processing_service.py` (pendiente→procesando→procesado/error) | CP-26 (Estados correctos) |
| RF-14 | HU-07 | CU-10 (Logs/Reprocesar) | Módulo Logs | `app/models/log_procesamiento.py`, `app/routers/dashboard.py:reprocesar_documento`, `app/services/processing_service.py` | CP-27 (Log errores), CP-28 (Reprocesar) | Parcial: reprocesamiento llama a método inexistente |

## RN (Reglas de Negocio) implementadas
| Regla | Descripción | Implementación |
|---|---|---|
| RN-01 | Contraseñas hasheadas (bcrypt) | `app/core/security.py:get_password_hash` + `passlib[bcrypt]` | Implementado en código; requiere prueba |
| RN-02 | API Keys en `.env` | `.env.example` + `.gitignore` excluye `.env` | Parcial: retirar valores por defecto y secretos de documentación |
| RN-03 | Validación archivo en backend | `app/routers/documents.py:validate_file` (tipo + tamaño) | Parcial: falta validación robusta de contenido/tamaño por streaming |
| RN-04 | Autorización por roles | `app/core/deps.py:require_admin`, `get_current_active_user` | Parcial: dashboard/logs no exigen `require_admin` |
| RN-05 | Arquitectura por capas | `routers/` → `services/` → `models/` |
| RN-06 | RAG no inventa respuestas | `app/services/ai_service.py:responder_pregunta` (prompt estricto + fallback) | Parcial: requiere validar recuperación y fuentes con ChromaDB compartido |

## Casos de prueba del plan 04-Pruebas (referencia)
| ID | Descripción | Requisitos cubiertos | Estado |
|---|---|---|---|
| CP-01 | Login con credenciales válidas | RF-01 | ✅ Implementado |
| CP-02 | Login con credenciales inválidas | RF-01 | ✅ Implementado |
| CP-03 | Acceso a endpoint protegido con token inválido | RF-01, RF-02 | ✅ Implementado |
| CP-04 | Usuario sin rol admin intenta crear usuario | RF-02 | ✅ Implementado |
| CP-05 | Crear repositorio como usuario autenticado | RF-03 | ✅ Implementado |
| CP-06 | Listar repositorios propios | RF-03 | ✅ Implementado |
| CP-07 | Actualizar repositorio propio | RF-03 | ✅ Implementado |
| CP-08 | Eliminar repositorio propio | RF-03 | ✅ Implementado |
| CP-09 | Subir PDF válido | RF-04, RN-03 | ✅ Implementado |
| CP-10 | Subir DOCX válido | RF-04, RN-03 | ✅ Implementado |
| CP-11 | Subir TXT válido | RF-04, RN-03 | ✅ Implementado |
| CP-12 | Rechazar archivo tipo no permitido | RF-04, RN-03 | ✅ Implementado |
| CP-13 | Rechazar archivo > 10 MB | RF-04, RN-03 | ✅ Implementado |
| CP-14 | Descargar documento | RF-05 | ✅ Implementado |
| CP-15 | Eliminar documento | RF-05 | ✅ Implementado |
| CP-16 | Listar documentos con filtros | RF-05 | ✅ Implementado |
| CP-17 | Extraer texto de PDF/DOCX/TXT | RF-06 | ✅ Implementado |
| CP-18 | Clasificar documento en 3+ categorías | RF-07 | ✅ Implementado |
| CP-19 | Generar resumen automático | RF-08 | ✅ Implementado |
| CP-20 | Extraer campos clave (3 tipos doc) | RF-09 | ✅ Implementado |
| CP-21 | Buscar por palabra clave en contenido | RF-10 | ✅ Implementado |
| CP-22 | Buscar por palabra clave en nombre | RF-10 | ✅ Implementado |
| CP-23 | Pregunta RAG con respuesta y fuentes | RF-11 | ✅ Implementado |
| CP-24 | Pregunta RAG sin info → "no encontré" | RF-11 | ✅ Implementado |
| CP-25 | Dashboard con indicadores | RF-12 | ✅ Implementado |
| CP-26 | Estados de procesamiento correctos | RF-13 | ✅ Implementado |
| CP-27 | Log de errores registrado | RF-14 | ✅ Implementado |
| CP-28 | Reprocesar documento en error | RF-14 | ✅ Implementado |

## Frontend - Casos de prueba de interfaz
| ID | Pantalla | Funcionalidad | Requisitos |
|---|---|---|---|
| FE-01 | Login | Formulario, validación, error handling, redirect | RF-01 |
| FE-02 | Repositories | Listar cards, crear modal, stats, eliminar | RF-03 |
| FE-03 | RepositoryDetail | Tabla docs, filtros, upload modal, acciones | RF-04, RF-05 |
| FE-04 | DocumentDetail | Metadatos, resumen, campos JSON, logs, descargar | RF-05, RF-07, RF-08, RF-09, RF-13 |
| FE-05 | Chat | Selector repo, historial, fuentes con similitud % | RF-11 |
| FE-06 | Dashboard | Cards métricas, gráficos barras, tabla errores, tabs | RF-12, RF-14 |

*(Matriz consolidada final — todos los requisitos funcionales RF-01 a RF-14 trazados a código y casos de prueba.)*