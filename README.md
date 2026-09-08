# IntelliDoc

Sistema web inteligente para gestionar, analizar y consultar documentos empresariales.

IntelliDoc permite organizar documentos en repositorios, subir archivos PDF/DOCX/TXT, extraer su contenido, clasificarlos, generar resúmenes y campos estructurados con un proveedor de IA configurable, y realizar consultas conversacionales con fuentes documentales.

## Funcionalidades

- Registro, inicio de sesión y autenticación JWT.
- Roles de administrador y usuario.
- Creación y gestión de repositorios.
- Carga, consulta, descarga y eliminación de documentos.
- Procesamiento de archivos PDF, DOCX y TXT.
- Extracción de texto, clasificación, resumen y extracción de campos.
- Búsqueda por palabras clave.
- Chat RAG con fuentes documentales.
- Dashboard con estadísticas y logs de procesamiento.
- Proveedor de IA intercambiable entre Gemini, OpenAI y Claude/Anthropic.

## Tecnologías

| Capa | Tecnologías |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, Axios, React Router |
| Backend | Python 3.11, FastAPI, SQLAlchemy, Alembic |
| Base de datos | MySQL 8.0+; compatible con MySQL externo de Clever Cloud |
| Búsqueda vectorial | ChromaDB persistente local |
| Embeddings | sentence-transformers |
| IA | Gemini, OpenAI o Claude/Anthropic |

## Estructura del repositorio

```text
proyecto-integrador-DAE/
├── 01-Analisis/                         # Requisitos y análisis
├── 02-Diseno/                           # Arquitectura y diseño
├── 03-Desarrollo/
│   ├── backend/                         # API FastAPI y procesamiento IA
│   └── frontend/                        # Aplicación React/Vite
├── 04-Pruebas/                          # Plan y casos de prueba
├── 05-Implementacion/                   # Documentación de implementación
├── 06-Manual-Usuario/                   # Manual de usuario
├── 07-Manual-Tecnico/                   # Manual técnico
├── 08-Matriz-Trazabilidad/              # Trazabilidad de requisitos
├── 09-Codigo-Fuente/                    # Documentación histórica del código
├── 10-Base-Datos/                       # Documentación de base de datos
├── 11-Repositorio-Documentos-Prueba/    # Documentos para pruebas
├── 12-Video/                            # Material audiovisual
├── 13-Presentacion/                     # Presentación del proyecto
└── README.md
```

El código ejecutable se encuentra en `03-Desarrollo/backend` y `03-Desarrollo/frontend`.

## Requisitos previos

- Python 3.11.
- Node.js 18+ y pnpm o npm.
- MySQL 8.0+ local o una instancia MySQL externa.
- Una API key de Gemini, OpenAI o Anthropic.

## Configurar el backend

Desde una terminal:

```bash
cd 03-Desarrollo/backend
python -m venv venv
```

Activar el entorno en Windows:

```powershell
venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear `.env` copiando `.env.example` y configurar las variables:

```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@host:3306/base_de_datos
SECRET_KEY=genera-una-clave-secreta-larga
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
CHROMADB_PATH=./chroma_db
LLM_PROVIDER=gemini
LLM_API_KEY=tu_api_key
LLM_MODEL=gemini-flash-latest
LLM_BASE_URL=
```

Para utilizar OpenAI:

```env
LLM_PROVIDER=openai
LLM_API_KEY=tu_api_key_de_openai
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=
```

Para utilizar Claude:

```env
LLM_PROVIDER=anthropic
LLM_API_KEY=tu_api_key_de_anthropic
LLM_MODEL=claude-3-5-haiku-latest
LLM_BASE_URL=
```

La clave de API nunca debe subirse a GitHub. El archivo `.env` está excluido mediante `.gitignore`.

Aplicar las migraciones:

```bash
alembic upgrade head
```

Iniciar la API:

```bash
uvicorn app.main:app --reload --port 8080
```

Endpoints útiles:

- API: http://localhost:8080
- Health check: http://localhost:8080/health
- Documentación Swagger: http://localhost:8080/docs

## Configurar el frontend

En otra terminal:

```bash
cd 03-Desarrollo/frontend
pnpm install
```

Crear `.env` con:

```env
VITE_API_URL=http://localhost:8080/api/v1
```

Iniciar la aplicación:

```bash
pnpm run dev
```

La interfaz estará disponible normalmente en http://localhost:5173.

Para generar una compilación de producción:

```bash
pnpm run build
```

## Base de datos externa

El backend puede conectarse a una base MySQL externa, por ejemplo Clever Cloud. La variable debe utilizar el controlador de SQLAlchemy para PyMySQL:

```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@host:3306/base_de_datos
```

Después de cambiar de base de datos, ejecutar siempre:

```bash
cd 03-Desarrollo/backend
alembic upgrade head
```

Esto crea las tablas de usuarios, repositorios, documentos, fragmentos, logs y consultas de chat.

## Flujo básico de uso

1. Iniciar el backend y el frontend.
2. Crear el primer usuario; se registra como administrador.
3. Crear un repositorio.
4. Subir un PDF, DOCX o TXT.
5. Esperar a que el documento alcance el estado `procesado`.
6. Consultar el resumen y los campos extraídos.
7. Realizar preguntas desde el chat.

## API principal

La API utiliza el prefijo `/api/v1`.

| Recurso | Operaciones principales |
|---|---|
| `/auth` | Registro, login, perfil y usuarios |
| `/repositories` | Crear, listar, actualizar y eliminar repositorios |
| `/documents` | Subir, listar, buscar, descargar y eliminar documentos |
| `/chat` | Preguntas y historial de conversaciones |
| `/dashboard` | Métricas, logs y reprocesamiento |

La especificación completa está disponible en Swagger en `/docs` cuando el backend está iniciado.

## Consideraciones actuales

- Los documentos originales se almacenan localmente en `03-Desarrollo/backend/storage`.
- ChromaDB se almacena localmente en `03-Desarrollo/backend/chroma_db`.
- Estos directorios no deben versionarse ni utilizarse como almacenamiento persistente en un despliegue serverless.
- Los archivos PDF escaneados requieren OCR, funcionalidad que no está incluida actualmente.
- El procesamiento de documentos se ejecuta de forma síncrona y puede tardar según el tamaño del archivo y el proveedor de IA.

## Documentación académica

- [Análisis](01-Analisis/01-Documento-Analisis.md)
- [Diseño](02-Diseno/02-Documento-Diseno.md)
- [Desarrollo](03-Desarrollo/README.md)
- [Plan de pruebas](04-Pruebas/04-Plan-Pruebas.md)
- [Implementación](05-Implementacion/05-Documento-Implementacion.md)
- [Manual de usuario](06-Manual-Usuario/06-Manual-Usuario.md)
- [Manual técnico](07-Manual-Tecnico/07-Manual-Tecnico.md)
- [Matriz de trazabilidad](08-Matriz-Trazabilidad/08-Matriz-Trazabilidad.md)
- [Base de datos](10-Base-Datos/README.md)
- [Documentos de prueba](11-Repositorio-Documentos-Prueba/README.md)

## Estado del proyecto

El sistema cuenta con un flujo funcional local de autenticación, repositorios, documentos, procesamiento IA, búsqueda, chat y dashboard. La validación completa debe realizarse con las credenciales y servicios configurados en el entorno local, sin publicar secretos en el repositorio.
