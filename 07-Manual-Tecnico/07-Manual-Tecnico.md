# 07 – Manual Técnico / de Administración
## Proyecto: IntelliDoc – Sistema Inteligente de Gestión y Análisis Documental

**Versión:** 1.1 | **Estado:** guía técnica de instalación y diagnóstico; validación limpia pendiente

---

## 1. Requisitos previos del sistema

| Componente | Versión mínima | Recomendada | Verificación |
|---|---|---|---|
| **Python** | 3.11 | 3.12.x | `python --version` |
| **Node.js** | 18.x | 22.x (LTS) | `node --version` |
| **npm** | 9.x | 10.x | `npm --version` |
| **MySQL** | 8.0 | 8.0.36+ | `mysql --version` |
| **Git** | 2.30+ | 2.45+ | `git --version` |
| **RAM** | 4 GB | 8 GB+ | `free -h` / Task Manager |
| **Disco** | 10 GB libres | 20 GB+ | `df -h` |

---

## 2. Instalación del Backend (FastAPI)

### 2.1 Crear entorno virtual
```bash
cd 09-Codigo-Fuente/backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2.2 Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencias críticas (versiones pinned):**
```
numpy==1.26.4
scipy==1.13.1
bcrypt==3.2.2
chromadb==0.4.22
```

### 2.3 Variables de entorno
```bash
cp .env.example .env
# Editar .env con valores reales:
# DATABASE_URL=mysql+pymysql://intellidoc:intellidoc@localhost:3306/intellidoc
# SECRET_KEY=<generar_con_secrets.token_urlsafe(32)>
# LLM_API_KEY=<tu_gemini_api_key>
# LLM_MODEL=gemini-flash-latest
```

### 2.4 Migraciones de base de datos
```bash
alembic upgrade head
```
**Verificación:**
```bash
mysql -u intellidoc -p intellidoc -e "SHOW TABLES;"
# Debe mostrar 7 tablas: alembic_version, usuarios, repositorios, documentos, fragmentos, logs_procesamiento, consultas_chat
```

### 2.5 Ejecutar servidor
```bash
# Desarrollo (con reload)
uvicorn app.main:app --reload --port 8000

# Producción (4 workers)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Verificación:**
- `curl http://localhost:8000/health` → `{"status":"ok"}`
- Swagger UI: `http://localhost:8000/docs`

---

## 3. Instalación del Frontend (React + Vite)

### 3.1 Instalar dependencias
```bash
cd 09-Codigo-Fuente/frontend
npm install
```

### 3.2 Variables de entorno
```bash
cp .env.example .env
# VITE_API_URL=http://localhost:8000/api/v1
```

### 3.2 Desarrollo
```bash
npm run dev
# → http://localhost:5173 (o 5174 si 5173 ocupado)
```

### 3.3 Build producción
```bash
npm run build
# Genera carpeta dist/ → servir con Nginx
```

---

## 4. Configuración de la Base de Datos (MySQL 8.0)

### 4.1 Crear base de datos y usuario
```sql
-- Conectar como root
mysql -u root -p

CREATE DATABASE intellidoc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'intellidoc'@'localhost' IDENTIFIED BY 'intellidoc';
GRANT ALL PRIVILEGES ON intellidoc.* TO 'intellidoc'@'localhost';
FLUSH PRIVILEGES;
```

### 4.2 Ejecutar migraciones (Alembic)
```bash
cd 09-Codigo-Fuente/backend
source venv/Scripts/activate
alembic upgrade head
```

### 4.3 Verificación manual
```sql
USE intellidoc;
SHOW TABLES;
-- Debe mostrar: alembic_version, usuarios, repositorios, documentos, fragmentos, logs_procesamiento, consultas_chat

DESCRIBE usuarios;
-- id CHAR(36) PK, correo UNIQUE, password_hash, rol, activo, creado_en
```

### 4.4 Script SQL directo (alternativa a Alembic)
Ver `10-Base-Datos/README.md` → sección "Opción 2: SQL directo (para MySQL 8.0+)"

---

## 5. Configuración del servicio de IA (Gemini)

### 5.1 Obtener API Key
1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Iniciar sesión con cuenta Google
3. **"Create API Key"** → Copiar clave
4. **Opcional:** Upgrade a plan pagado para cuota >5 req/min

### 5.2 Configurar en `.env`
```env
LLM_PROVIDER=gemini
LLM_API_KEY=<tu_gemini_api_key_local>
LLM_MODEL=gemini-flash-latest
```

### 5.3 Modelos disponibles (verificar con `genai.list_models()`)
| Modelo | Métodos | Notas |
|---|---|---|
| `gemini-flash-latest` | generateContent | Recomendado (alias a 3.8-flash) |
| `gemini-2.5-flash` | generateContent | Rápido, buena calidad |
| `gemini-2.5-pro` | generateContent | Más preciso, más lento |
| `gemini-pro` | ❌ NO DISPONIBLE | Deprecated |

### 5.3 Verificar configuración
```bash
cd backend
source venv/Scripts/activate
python -c "
from app.services.ai_service import AIService
ai = AIService()
print('Modelo:', ai.model.model_name if ai.model else 'NO INICIALIZADO')
print('Clasificar test:', ai.clasificar('Contrato de arrendamiento'))
"
```

---

## 6. Administración de usuarios

### 6.1 Crear primer administrador (seed)
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Admin","correo":"admin@empresa.com","password":"ClaveSegura123","rol":"administrador"}'
```
> **Nota:** El primer usuario registrado se convierte automáticamente en **Administrador**.

### 6.2 Gestión via API (solo Admin)
```bash
# Listar usuarios
curl -H "Authorization: Bearer <TOKEN_ADMIN>" http://localhost:8000/api/v1/auth/users

# Crear usuario (Admin)
curl -X POST -H "Authorization: Bearer <TOKEN_ADMIN>" -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","correo":"juan@empresa.com","password":"Pass1234","rol":"usuario"}' \
  http://localhost:8000/api/v1/auth/users

# Desactivar usuario
curl -X PUT -H "Authorization: Bearer <TOKEN_ADMIN>" -H "Content-Type: application/json" \
  -d '{"activo":false}' http://localhost:8000/api/v1/auth/users/{USER_ID}
```

### 6.3 Roles y permisos
| Acción | Administrador | Usuario |
|---|---|---|
| Ver todos los usuarios | ✅ | ❌ |
| Crear usuarios | ✅ | ❌ |
| Editar/desactivar usuarios | ✅ | Solo propio perfil |
| Eliminar usuarios | ✅ | ❌ |
| Ver dashboard global | ✅ | ❌ |
| Ver logs de error globales | ✅ | ❌ |
| Reprocesar cualquier doc | ✅ | Solo propios (si admin) |
| Gestionar repositorios | Todos | Solo propios |

---

## 7. Monitoreo y logs

### 7.1 Logs de procesamiento (Tabla `logs_procesamiento`)
```sql
SELECT * FROM logs_procesamiento ORDER BY creado_en DESC LIMIT 20;
```
**Tipos de log:**
- `inicio_procesamiento`, `extraccion_texto`, `chunking`, `embeddings`, `almacenamiento`, `ia_completado`, `completado`
- `error_extraccion_texto`, `error_chunking`, `error_embeddings`, `error_almacenamiento`, `error_ia`, `error_background`

### 7.2 Logs de aplicación (consola uvicorn)
```bash
# Desarrollo: salida en consola
uvicorn app.main:app --reload --port 8000 --log-level info

# Producción: logs a archivo
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/intellidoc/access.log \
  --error-logfile /var/log/intellidoc/error.log \
  --log-level info
```

### 7.3 Logs de ChromaDB
```bash
# EphemeralClient: logs en memoria (se pierden al reiniciar)
# Para persistencia: cambiar a PersistentClient en processing_service.py
```

### 7.4 Logs de MySQL
```bash
# Error log
tail -f /var/log/mysql/error.log

# Slow query log (activar en my.cnf)
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

---

## 8. Reprocesamiento de documentos en error

### 8.1 Desde Dashboard (Admin)
1. Ir a **Dashboard** → Pestaña **Logs** o **Resumen**
2. Localizar documento con error (badge rojo)
3. Click botón **"Reprocesar" 🔄**
4. Sistema: `Error` → `Pendiente` → `Procesando` → `Procesado` / `Error`

### 8.2 Via API (Admin)
```bash
curl -X POST -H "Authorization: Bearer <TOKEN_ADMIN>" \
  http://localhost:8000/api/v1/dashboard/documents/{DOC_ID}/reprocess
```

### 8.3 Causas comunes de error y solución
| Error en log | Causa | Solución |
|---|---|---|
| `LLM API error: 401 Invalid API key` | API key inválida/expirada | Verificar `.env` → `LLM_API_KEY` |
| `LLM API error: 429 Quota exceeded` | Cuota free tier agotada (5 req/min) | Esperar 1 min / Upgrade plan / Usar otra key |
| `PDF corrupto / no text extracted` | PDF escaneado / corrupto | Verificar PDF original / Usar OCR externo |
| `Chunking failed: empty text` | Archivo vacío / sin texto | Verificar archivo original |
| `ChromaDB error: collection not found` | Colección no existe | Reiniciar backend (EphemeralClient recrea) |
| `MySQL connection refused` | BD caída / credenciales | Verificar MySQL corriendo + credenciales .env |

---

## 9. Solución de problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| **Login 422 "Unprocessable Entity"** | Frontend envía JSON, backend espera FormData | ✅ Fix: `api.js` usa `FormData` para login/register |
| **Register 400 "password >72 bytes"** | bcrypt 5.x límite 72 bytes | ✅ `pip install "bcrypt<4.0"` (v3.2.2) |
| **ChromaDB compila C++ (hnswlib)** | Windows sin Visual C++ Build Tools | ✅ Usar `EphemeralClient` (Python puro) |
| **numpy 2.x / scipy 1.18+ error** | Incompatibilidad ChromaDB | ✅ Pin `numpy==1.26.4`, `scipy==1.13.1` |
| **MySQL UUID error** | PostgreSQL UUID vs MySQL CHAR(36) | ✅ Type decorator `GUID` (CHAR(36) MySQL) |
| **Login 401 "Not authenticated"** | Token expirado / mal formado | Verificar `SECRET_KEY`, expiración 8 días |
| **CORS error en frontend** | Puerto frontend no en CORS | `.env`: `BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]` |
| **Layout en blanco tras login** | Layout lee localStorage antes de setear | ✅ Fix: `window.location.href = '/repositories'` tras login |
| **Gemini 404 "model not found"** | Modelo deprecated (1.5-flash, 1.5-pro, 2.5-flash) | ✅ Usar `gemini-flash-latest` (→ 3.8-flash) |
| **Gemini 429 Quota exceeded** | Free tier: 5 req/min | Esperar 1 min / Nueva API key / Plan pagado |

---

## 10. Mantenimiento y actualizaciones

### 10.1 Actualizar dependencias Python
```bash
cd backend
source venv/Scripts/activate
pip list --outdated
pip install --upgrade -r requirements.txt  # Cuidado: romper cambios
# Mejor: actualizar selectivamente
pip install --upgrade fastapi uvicorn pydantic sqlalchemy
```

### 10.2 Actualizar dependencias Node.js
```bash
cd frontend
npm outdated
npm update
# O selectivo:
npm update react react-dom react-router-dom axios
```

### 10.3 Rotación de logs
```bash
# Logrotate config (/etc/logrotate.d/intellidoc)
/var/log/intellidoc/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 640 intellidoc intellidoc
}
```

### 10.3 Limpieza de almacenamiento
```bash
# Limpiar archivos temporales (cron semanal)
find /tmp -name "intellidoc_*" -mtime +7 -delete

# Limpiar uploads huérfanos (docs eliminados en BD pero archivo queda)
# Script personalizado: comparar BD vs storage/
```

---

## 11. Respaldos y recuperación

> Los respaldos documentados cubren MySQL y `storage/`, pero no los vectores porque el código actual usa `EphemeralClient`. La recuperación completa exige persistir ChromaDB o ejecutar una reindexación comprobada.

### 11.1 Backup automatizado (cron diario 02:00)
```bash
#!/bin/bash
# /usr/local/bin/backup_intellidoc.sh
DATE=$(date +%F_%H-%M)
DB_BACKUP="/backups/db/intellidoc_${DATE}.sql"
STORAGE_BACKUP="/backups/storage/storage_${DATE}.tar.gz"

# DB
mysqldump -u intellidoc -p'intellidoc' intellidoc > ${DB_BACKUP}
gzip ${DB_BACKUP}

# Storage
tar -czf ${STORAGE_BACKUP} /path/to/09-Codigo-Fuente/backend/storage/

# Limpiar > 30 días
find /backups -name "*.sql.gz" -mtime +30 -delete
find /backups -name "storage_*.tar.gz" -mtime +30 -delete
```

```bash
# Crontab (root)
0 2 * * * /usr/local/bin/backup_intellidoc.sh
```

### 11.2 Restauración
```bash
# BD
gunzip -c /backups/db/intellidoc_2025-09-07.sql.gz | mysql -u intellidoc -p intellidoc

# Storage
tar -xzf /backups/storage/storage_2025-09-07.tar.gz -C /
```

### 11.3 Prueba de restauración (trimestral)
1. Restaurar en servidor de pruebas
2. Verificar login, carga doc, chat RAG
3. Documentar tiempo de recuperación (RTO)

---

## 12. Escalabilidad y límites conocidos

| Componente | Límite actual | Escalamiento |
|---|---|---|
| **Documentos** | ~100 (tested) | ChromaDB Persistent + BD dedicada |
| **Tamaño archivo** | 10 MB | Aumentar `MAX_FILE_SIZE` + streaming upload |
| **Usuarios concurrentes** | ~20 (dev) | Gunicorn workers + Redis session store |
| **ChromaDB Ephemeral** | Volátil | `PersistentClient(path="./chroma_db")` |
| **Gemini API** | 5 req/min free | Plan pagado / Múltiples keys round-robin |
| **Embeddings** | Local (CPU) | GPU + batch processing para miles |

---

## 12. Contactos y escalamiento

| Nivel | Contacto | Canal | SLA |
|---|---|---|---|
| **Nivel 1 - Soporte usuario** | Admin local | Email/Teams | 4h |
| **Nivel 2 - Técnico** | Dev team | Jira/Slack | 2h |
| **Nivel 3 - Infra/IA** | Arquitecto | Teléfono | 1h |

---

*Manual técnico actualizado para separar procedimiento esperado de pasos verificados. La instalación limpia debe ejecutarse y registrarse antes de declarar reproducibilidad.*