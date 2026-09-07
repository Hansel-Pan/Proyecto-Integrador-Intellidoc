# 10 – Base de Datos

Scripts SQL y migraciones para reproducir el modelo de datos de IntelliDoc.

## Estado
✅ Migración inicial generada con Alembic (versión actual)

## Estructura de tablas (modelo entidad-relación)

### 1. `usuarios`
| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | UUID (CHAR(36)) | PK |
| nombre | varchar(150) | NOT NULL |
| correo | varchar(255) | NOT NULL, UNIQUE |
| password_hash | varchar(255) | NOT NULL |
| rol | varchar(20) | NOT NULL, DEFAULT 'usuario' |
| activo | boolean | NOT NULL, DEFAULT true |
| creado_en | datetime | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

### 2. `repositorios`
| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | UUID (CHAR(36)) | PK |
| nombre | varchar(150) | NOT NULL |
| usuario_creador_id | UUID (CHAR(36)) | NOT NULL, FK → usuarios.id (CASCADE) |
| creado_en | datetime | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

### 3. `documentos`
| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | UUID (CHAR(36)) | PK |
| repositorio_id | UUID (CHAR(36)) | NOT NULL, FK → repositorios.id (CASCADE) |
| usuario_carga_id | UUID (CHAR(36)) | NOT NULL, FK → usuarios.id (CASCADE) |
| nombre_archivo | varchar(255) | NOT NULL |
| formato | varchar(10) | NOT NULL (pdf/docx/txt) |
| ruta_almacenamiento | varchar(500) | NOT NULL |
| estado | varchar(20) | NOT NULL, DEFAULT 'pendiente' |
| categoria | varchar(50) | NULL |
| resumen | text | NULL |
| campos_extraidos | json | NULL |
| creado_en | datetime | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| procesado_en | datetime | NULL |

### 4. `fragmentos`
| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | UUID (CHAR(36)) | PK |
| documento_id | UUID (CHAR(36)) | NOT NULL, FK → documentos.id (CASCADE) |
| texto | text | NOT NULL |
| vector_id | varchar(100) | NOT NULL, UNIQUE |
| orden | integer | NOT NULL |

### 5. `logs_procesamiento`
| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | UUID (CHAR(36)) | PK |
| documento_id | UUID (CHAR(36)) | NOT NULL, FK → documentos.id (CASCADE) |
| tipo | varchar(50) | NOT NULL |
| mensaje | text | NOT NULL |
| creado_en | datetime | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

### 6. `consultas_chat`
| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | UUID (CHAR(36)) | PK |
| usuario_id | UUID (CHAR(36)) | NOT NULL, FK → usuarios.id (CASCADE) |
| pregunta | text | NOT NULL |
| respuesta | text | NOT NULL |
| documentos_fuente | json | NULL |
| creado_en | datetime | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

## Índices creados
- `ix_usuarios_correo` (único) en `usuarios.correo`
- `ix_consultas_chat_usuario_id` en `consultas_chat.usuario_id`
- `ix_documentos_categoria` en `documentos.categoria`
- `ix_documentos_estado` en `documentos.estado`
- `ix_fragmentos_documento_id` en `fragmentos.documento_id`
- `ix_fragmentos_vector_id` (único) en `fragmentos.vector_id`
- `ix_logs_procesamiento_documento_id` en `logs_procesamiento.documento_id`
- `ix_logs_procesamiento_tipo` en `logs_procesamiento.tipo`

## Relaciones
- `usuarios` 1:N `repositorios` (usuario_creador)
- `usuarios` 1:N `documentos` (usuario_carga)
- `repositorios` 1:N `documentos`
- `documentos` 1:N `fragmentos`
- `documentos` 1:N `logs_procesamiento`
- `usuarios` 1:N `consultas_chat`

## Cómo aplicar la migración

### Opción 1: Con Alembic (recomendado)
```bash
cd 09-Codigo-Fuente/backend
# Configurar DATABASE_URL en .env (mysql+pymysql://user:pass@host:3306/db)
alembic upgrade head
```

### Opción 2: SQL directo (para MySQL 8.0+)
Ejecutar el siguiente script en orden:

```sql
-- Tabla usuarios
CREATE TABLE usuarios (
    id CHAR(36) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'usuario',
    activo BOOLEAN NOT NULL DEFAULT true,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla repositorios
CREATE TABLE repositorios (
    id CHAR(36) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    usuario_creador_id CHAR(36) NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_creador_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla documentos
CREATE TABLE documentos (
    id CHAR(36) PRIMARY KEY,
    repositorio_id CHAR(36) NOT NULL,
    usuario_carga_id CHAR(36) NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    formato VARCHAR(10) NOT NULL,
    ruta_almacenamiento VARCHAR(500) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    categoria VARCHAR(50),
    resumen TEXT,
    campos_extraidos JSON,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    procesado_en DATETIME,
    FOREIGN KEY (repositorio_id) REFERENCES repositorios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_carga_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla fragmentos
CREATE TABLE fragmentos (
    id CHAR(36) PRIMARY KEY,
    documento_id CHAR(36) NOT NULL,
    texto TEXT NOT NULL,
    vector_id VARCHAR(100) NOT NULL UNIQUE,
    orden INTEGER NOT NULL,
    FOREIGN KEY (documento_id) REFERENCES documentos(id) ON DELETE CASCADE
);

-- Tabla logs_procesamiento
CREATE TABLE logs_procesamiento (
    id CHAR(36) PRIMARY KEY,
    documento_id CHAR(36) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (documento_id) REFERENCES documentos(id) ON DELETE CASCADE
);

-- Tabla consultas_chat
CREATE TABLE consultas_chat (
    id CHAR(36) PRIMARY KEY,
    usuario_id CHAR(36) NOT NULL,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    documentos_fuente JSON,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX ix_usuarios_correo ON usuarios(correo);
CREATE INDEX ix_consultas_chat_usuario_id ON consultas_chat(usuario_id);
CREATE INDEX ix_documentos_categoria ON documentos(categoria);
CREATE INDEX ix_documentos_estado ON documentos(estado);
CREATE INDEX ix_fragmentos_documento_id ON fragmentos(documento_id);
CREATE UNIQUE INDEX ix_fragmentos_vector_id ON fragmentos(vector_id);
CREATE INDEX ix_logs_procesamiento_documento_id ON logs_procesamiento(documento_id);
CREATE INDEX ix_logs_procesamiento_tipo ON logs_procesamiento(tipo);
```

## Archivos de migración Alembic
- `09-Codigo-Fuente/backend/alembic/versions/` — Migración inicial para MySQL

## Notas
- La base de datos objetivo es **MySQL 8.0+**
- Los UUIDs se almacenan como `CHAR(36)` (compatibilidad MySQL)
- Los timestamps usan `DATETIME`
- Los campos JSON (`campos_extraidos`, `documentos_fuente`) usan tipo `JSON` nativo de MySQL 8.0+
- Las FK tienen `ON DELETE CASCADE` para limpieza automática
- Requiere `pymysql` como driver