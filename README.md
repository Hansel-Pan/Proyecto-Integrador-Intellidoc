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

- Git.
- Python 3.11. En Windows se recomienda instalarlo desde [python.org](https://www.python.org/downloads/release/python-3119/), porque la versión de ChromaDB incluida necesita sus paquetes compatibles.
- Node.js 18+ y npm.
- MySQL 8.0+ local o una instancia MySQL externa.
- Una API key de Gemini, OpenAI o Anthropic.

## Ejecutar el proyecto después de clonarlo

Estos pasos preparan una instalación nueva en otro equipo. Los comandos de Windows usan PowerShell; las rutas deben ejecutarse desde la raíz del repositorio clonado.

### 1. Clonar el repositorio

```powershell
git clone URL_DEL_REPOSITORIO
cd Proyecto-Integrador-Intellidoc
```

No se clonan los entornos virtuales, `node_modules`, archivos `.env`, documentos cargados ni la base vectorial local. Deben crearse/configurarse en el equipo nuevo.

### 2. Preparar MySQL

Inicia MySQL y crea una base de datos vacía. Por ejemplo, desde el cliente de MySQL:

```sql
CREATE DATABASE intellidoc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

También puede utilizarse una base MySQL externa. Se necesita conocer el usuario, contraseña, host, puerto y nombre exacto de la base. La URL debe incluir siempre el nombre después del último `/`:

```text
mysql+pymysql://usuario:contrasena@host:3306/nombre_de_base
```

### 3. Preparar el backend

```powershell
cd 03-Desarrollo/backend
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `03-Desarrollo/backend/.env` y configura como mínimo:

```env
DATABASE_URL=mysql+pymysql://usuario:contrasena@host:3306/nombre_de_base
SECRET_KEY=una-clave-secreta-larga-y-unica
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
LLM_PROVIDER=gemini
LLM_API_KEY=tu_api_key
LLM_MODEL=gemini-flash-latest
```

Si se usa OpenAI o Anthropic, cambia `LLM_PROVIDER`, `LLM_API_KEY` y `LLM_MODEL` según los ejemplos del archivo. No subas `.env` a GitHub.

### 4. Crear las tablas

Con el entorno virtual activo y ubicado en `03-Desarrollo/backend`, ejecuta:

```powershell
python -m alembic upgrade head
```

Este comando aplica las migraciones y crea las tablas de usuarios, repositorios, documentos, fragmentos, logs y consultas de chat. Si aparece un error indicando `database=''` o `schema is None`, revisa que `DATABASE_URL` termine en `/nombre_de_base`.

### 5. Verificar y arrancar el backend

Opcionalmente, verifica la instalación:

```powershell
python verify_install.py
```

Mantén abierta esta primera terminal e inicia la API:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Comprueba que responde abriendo [http://localhost:8000/health](http://localhost:8000/health). También están disponibles [Swagger](http://localhost:8000/docs) y la API en `http://localhost:8000/api/v1`.

### 6. Preparar y arrancar el frontend

Abre una segunda terminal desde la raíz del repositorio:

```powershell
cd 03-Desarrollo/frontend
npm install
Copy-Item .env.example .env
```

Comprueba que `03-Desarrollo/frontend/.env` contenga:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Inicia la interfaz:

```powershell
npm run dev
```

Abre la URL que muestre Vite, normalmente [http://localhost:5173](http://localhost:5173). Deben permanecer abiertas las dos terminales: una para FastAPI y otra para Vite.

### 7. Primer uso

1. Abre la aplicación en el navegador.
2. Registra el primer usuario; el sistema lo crea como administrador.
3. Crea un repositorio.
4. Sube un PDF, DOCX o TXT.
5. Espera a que el documento quede en estado `procesado`.
6. Prueba el resumen, la búsqueda y el chat.

### Comandos equivalentes en Linux, macOS o Git Bash

Desde `03-Desarrollo/backend`, sustituye la activación de PowerShell por:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m alembic upgrade head
python -m uvicorn app.main:app --reload --port 8000
```

En otra terminal, instala y arranca el frontend con `npm install` y `npm run dev`.

## Configurar el backend

La guía completa para una instalación nueva está en [Ejecutar el proyecto después de clonarlo](#ejecutar-el-proyecto-despues-de-clonarlo). Esta sección resume la configuración de variables.

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

El backend se inicia en el puerto `8000`:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Endpoints útiles:

- API: http://localhost:8000
- Health check: http://localhost:8000/health
- Documentación Swagger: http://localhost:8000/docs

## Configurar el frontend

En otra terminal:

```bash
cd 03-Desarrollo/frontend
npm install
```

Crear `.env` con:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

Iniciar la aplicación:

```bash
npm run dev
```

La interfaz estará disponible normalmente en http://localhost:5173.

Para generar una compilación de producción:

```bash
npm run build
```

## Base de datos externa

El backend puede conectarse a una base MySQL externa, por ejemplo Clever Cloud. La variable debe utilizar el controlador de SQLAlchemy para PyMySQL:

```env
DATABASE_URL=mysql+pymysql://usuario:contrasena@host:3306/base_de_datos
```

Después de cambiar de base de datos, ejecutar siempre:

```bash
cd 03-Desarrollo/backend
python -m alembic upgrade head
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
