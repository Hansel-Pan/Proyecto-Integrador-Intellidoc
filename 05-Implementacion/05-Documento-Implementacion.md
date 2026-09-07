# 05 – Documento de Implementación y Despliegue
## Proyecto: IntelliDoc

**Estado:** 🟡 **Guía preparada** — El despliegue local está documentado, pero la ejecución limpia y las evidencias deben completarse antes de declarar el sistema reproducible.

---

## 1. Ambiente de implementación

| Componente | Especificación |
|---|---|
| **SO Servidor** | Windows 11 Pro (Build 22631) |
| **CPU** | Intel Core i7-11700 / AMD Ryzen 7 5800H (4+ cores) |
| **RAM** | 16 GB DDR4 (mínimo 4 GB, recomendado 8 GB+) |
| **Disco** | SSD 256 GB libres (BD + ChromaDB + almacenamiento archivos) |
| **Python** | 3.12.10 (venv aislado) |
| **Node.js** | 22.20.0 (LTS) |
| **MySQL** | 8.0.36 (puerto 3306) |
| **Navegador** | Chrome 128+, Edge 128+, Firefox 129+ |

---

## 2. Configuración de base de datos y almacenamiento

### 2.1 Base de datos MySQL 8.0
```bash
# Crear BD y usuario
mysql -u root -p
CREATE DATABASE intellidoc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'intellidoc'@'localhost' IDENTIFIED BY 'intellidoc';
GRANT ALL PRIVILEGES ON intellidoc.* TO 'intellidoc'@'localhost';
FLUSH PRIVILEGES;
```

### 2.2 Migraciones Alembic
```bash
cd 09-Codigo-Fuente/backend
source venv/Scripts/activate
alembic upgrade head
```

**Tablas creadas (6):**
| Tabla | Registros iniciales |
|---|---|
| usuarios | 1 (admin seed) |
| repositorios | 0 |
| documentos | 0 |
| fragmentos | 0 |
| logs_procesamiento | 0 |
| consultas_chat | 0 |

### 2.3 Almacenamiento de archivos
```
09-Codigo-Fuente/backend/storage/
├── {user_id}_{repo_id}_{filename}.pdf
├── {user_id}_{repo_id}_{filename}.docx
└── {user_id}_{repo_id}_{filename}.txt
```
- Permisos: Lectura/Escritura solo usuario que ejecuta backend
- Sanitización: `{user_id}_{repo_id}_{original_filename}` evita path traversal

---

## 3. Configuración de servicios de IA

### 3.1 Proveedor LLM: Google Gemini
- **Modelo:** `gemini-flash-latest` (resuelve a `gemini-3.8-flash`)
- **API Key:** Obtenida en [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Cuota free tier:** 5 req/min (plan pagado recomendado para producción)

### 3.2 Embeddings locales
- **Modelo:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensión:** 384
- **Ejecutado localmente** (sin API externa, sin costo, sin latencia red)

### 3.3 Vector Store: ChromaDB
- **Modo:** `EphemeralClient` (en memoria, sin compilación C++)
- **Colección:** `documentos` (cosine space)
- **Persistencia:** Volátil (se pierde al reiniciar backend) — documentado como limitación

---

## 4. Variables de entorno y configuración segura

### 4.1 Archivo `backend/.env` (NUNCA en Git)
```env
PROJECT_NAME=IntelliDoc
VERSION=1.0.0
API_V1_STR=/api/v1

BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:5174","http://localhost:3000"]

# MySQL Configuration
DATABASE_URL=mysql+pymysql://intellidoc:intellidoc@localhost:3306/intellidoc
CHROMADB_PATH=./chroma_db

SECRET_KEY=tu_clave_secreta_de_al_menos_32_caracteres_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# Gemini AI Configuration
LLM_PROVIDER=gemini
LLM_API_KEY=<configurar localmente; nunca publicar la clave>
LLM_MODEL=gemini-flash-latest
LLM_BASE_URL=

EMBEDDING_MODEL=all-MiniLM-L6-v2

MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=["pdf","docx","txt"]
```

### 4.2 Archivo `frontend/.env`
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 4.3 Seguridad
- `.env` en `.gitignore` (backend y frontend)
- `SECRET_KEY` generada con `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `LLM_API_KEY` nunca hardcodeada, solo variable de entorno
- Contraseñas: bcrypt hash (nunca texto plano)

---

## 5. Proceso de instalación

### 5.1 Backend
```bash
cd 09-Codigo-Fuente/backend

# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores reales (ver sección 4)

# 4. Ejecutar migraciones
alembic upgrade head

# 5. Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

**Verificación:**
- `http://localhost:8000/health` → `{"status":"ok"}`
- `http://localhost:8000/docs` → Swagger UI

### 5.2 Frontend
```bash
cd 09-Codigo-Fuente/frontend

# 1. Instalar dependencias
npm install

# 2. Configurar variables
cp .env.example .env

# 2. Desarrollo
npm run dev
```

**Verificación:**
- `http://localhost:5173` (o 5174) → Pantalla login IntelliDoc

---

## 6. Proceso de despliegue (producción local)

### 6.1 Build frontend
```bash
cd frontend
npm run build
# Genera carpeta dist/ lista para servir con Nginx
```

### 6.2 Backend producción
```bash
# Opción A: Uvicorn directo (desarrollo)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Opción B: Gunicorn + Uvicorn workers (producción)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 6.3 Nginx reverse proxy (producción)
```nginx
server {
    listen 80;
    server_name localhost;

    # Frontend estático
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 7. URL y mecanismo de acceso

| Entorno | URL | Descripción |
|---|---|---|
| **Desarrollo Frontend** | `http://localhost:5173` | Vite dev server + HMR |
| **Desarrollo Backend** | `http://localhost:8000` | Uvicorn + reload |
| **API Docs (Swagger)** | `http://localhost:8000/docs` | OpenAPI interactivo |
| **Producción (Nginx)** | `http://localhost` | Puerto 80 → Frontend + `/api/` → Backend |

---

## 8. Manual de usuario
**Ver documento:** `06-Manual-Usuario/06-Manual-Usuario.md`

---

## 9. Manual de administración o soporte
**Ver documento:** `07-Manual-Tecnico/07-Manual-Tecnico.md`

---

## 10. Estrategia básica de respaldo y recuperación

### 10.1 Base de datos (MySQL)
```bash
# Backup diario (cron 02:00)
mysqldump -u intellidoc -p intellidoc > /backups/intellidoc_$(date +%F).sql

# Restauración
mysql -u intellidoc -p intellidoc < /backups/intellidoc_2025-09-07.sql
```

### 10.2 Almacenamiento archivos
```bash
# Backup semanal
tar -czf /backups/storage_$(date +%F).tar.gz 09-Codigo-Fuente/backend/storage/
```

### 10.3 ChromaDB (Ephemeral)
- **No se respalda actualmente:** `EphemeralClient` mantiene los vectores solo en memoria y los pierde al reiniciar.
- Antes de usar esta estrategia en producción, migrar a `PersistentClient(path="./chroma_db")` o a una base vectorial administrada y probar restauración/reindexación.

### 10.4 Recuperación ante desastres (RTO/RPO)
| Escenario | RTO | RPO | Procedimiento |
|---|---|---|---|
| Fallo BD | <30 min | 24h | Restaurar `mysqldump` + reiniciar backend |
| Fallo servidor | <1 hora | 1 semana | Reinstalar en nuevo servidor, restaurar BD + storage |
| Corrupción ChromaDB | <5 min | 0 | Reiniciar backend (se regenera al reprocesar) |

---

## 11. Plan básico de mantenimiento

| Frecuencia | Tarea | Responsable |
|---|---|---|
| **Diaria** | Revisar logs `logs_procesamiento` (errores) | Admin |
| **Semanal** | Verificar espacio disco (`df -h`), limpiar temp | Admin |
| **Quincenal** | `pip list --outdated` / `npm outdated` | Dev |
| **Mensual** | Rotar logs, revisar cuota Gemini API | Admin |
| **Trimestral** | Actualizar dependencias (patch), revisar CVE | Dev |

---

## 12. Evidencias del sistema funcionando

### 12.1 Capturas de pantalla (carpeta `05-Implementacion/evidencias/`)

| Archivo | Descripción |
|---|---|
| `login_page.png` | Pantalla login con validación |
| `repositories_list.png` | Lista repositorios con stats |
| `repo_detail_upload.png` | Modal upload + tabla documentos |
| `doc_detail_ia.png` | Categoría, resumen, campos JSON, logs |
| `chat_rag_sources.png` | Chat con respuesta + 3 fuentes % similitud |
| `dashboard_metrics.png` | Cards, gráficos barras, tabla errores |
| `logs_table.png` | Logs paginados con filtros |
| `swagger_docs.png` | Swagger UI con todos endpoints |

### 12.2 URLs de acceso (entorno actual)
```
Frontend:  http://localhost:5173
Backend:   http://localhost:8000
Swagger:   http://localhost:8000/docs
Health:    http://localhost:8000/health
```

### 12.3 Credenciales de prueba (solo entorno local)
| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | Crear localmente | No publicar credenciales reales |
| Usuario | Crear localmente | No publicar credenciales reales |

---

## 13. Reproducibilidad garantizada

La reproducción queda **pendiente de validación en máquina limpia**. Los pasos de la sección 5 describen el procedimiento esperado con:
1. Windows 10/11 o Linux (WSL2)
2. MySQL 8.0+ instalado y corriendo
3. Python 3.12+, Node.js 18+
4. API Key Gemini válida

**Tiempo estimado setup limpio:** 15-20 minutos

---

*Documento actualizado: la ejecución limpia, las evidencias y la validación end-to-end deben registrarse antes de declarar el despliegue verificado.*