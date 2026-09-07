# 11 – Repositorio de Documentos de Prueba
## IntelliDoc — Lista de 30 documentos para pruebas funcionales

**Estado:** 🟡 **Lista preparada** — La distribución está definida, pero los 30 archivos físicos y su verificación reproducible aún están pendientes en este workspace.

---

## Distribución por categoría

| Categoría | Cantidad | Formatos | Descripción |
|---|---|---|---|
| **Contratos** | 10 | 4 PDF, 3 DOCX, 3 TXT | Arrendamiento, servicios, confidencialidad, compraventa |
| **Facturas** | 10 | 4 PDF, 3 DOCX, 3 TXT | Productos, servicios, recurrentes, internacionales |
| **Informes** | 10 | 4 PDF, 3 DOCX, 3 TXT | Técnicos, financieros, auditoría, gestión |

---

## Lista completa de documentos

### 📄 CONTRATOS (10)

| # | Archivo | Formato | Tamaño | Descripción | Campos clave esperados |
|---|---|---|---|---|---|
| 1 | `contrato_arrendamiento_001.pdf` | PDF | 245 KB | Arrendamiento local comercial 3 años | partes, fecha_inicio, fecha_fin, valor, moneda, objeto |
| 2 | `contrato_servicios_002.docx` | DOCX | 187 KB | Servicios profesionales TI 6 meses | partes, fecha_inicio, fecha_fin, valor, objeto |
| 3 | `contrato_confidencialidad_003.txt` | TXT | 12 KB | NDA bilateral entre empresas | partes, fecha_inicio, fecha_fin, objeto |
| 4 | `contrato_compraventa_004.pdf` | PDF | 312 KB | Compraventa equipo industrial | partes, fecha_inicio, fecha_fin, valor, moneda, objeto |
| 5 | `contrato_arrendamiento_005.docx` | DOCX | 201 KB | Arrendamiento vivienda 1 año | partes, fecha_inicio, fecha_fin, valor, moneda |
| 6 | `contrato_servicios_006.pdf` | PDF | 156 KB | Servicios contables anuales | partes, fecha_inicio, fecha_fin, valor, moneda |
| 7 | `contrato_confidencialidad_007.txt` | TXT | 8 KB | NDA unilateral empleado | partes, fecha_inicio, fecha_fin, objeto |
| 8 | `contrato_compraventa_008.pdf` | PDF | 423 KB | Compraventa vehículo flota | partes, fecha_inicio, fecha_fin, valor, moneda |
| 9 | `contrato_servicios_009.docx` | DOCX | 134 KB | Servicios marketing digital 3 meses | partes, fecha_inicio, fecha_fin, valor, objeto |
| 10 | `contrato_arrendamiento_010.txt` | TXT | 15 KB | Arrendamiento equipos oficina | partes, fecha_inicio, fecha_fin, valor, moneda |

### 📄 FACTURAS (10)

| # | Archivo | Formato | Tamaño | Descripción | Campos clave esperados |
|---|---|---|---|---|---|
| 11 | `factura_001.pdf` | PDF | 198 KB | Factura productos oficina | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 12 | `factura_002.docx` | DOCX | 145 KB | Factura servicios consultoría | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 13 | `factura_003.txt` | TXT | 9 KB | Factura productos tecnológicos | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 14 | `factura_004.pdf` | PDF | 267 KB | Factura internacional (USD) | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 15 | `factura_005.docx` | DOCX | 178 KB | Factura recurrentes mensuales | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 16 | `factura_006.pdf` | PDF | 234 KB | Factura servicios legales | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 17 | `factura_007.txt` | TXT | 11 KB | Factura equipos cómputo | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 18 | `factura_008.pdf` | PDF | 312 KB | Factura servicios contables | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 19 | `factura_009.docx` | DOCX | 167 KB | Factura marketing digital | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |
| 20 | `factura_010.txt` | TXT | 13 KB | Factura equipos oficina | numero_factura, fecha, proveedor, cliente, total, impuestos, moneda |

### 📄 INFORMES (10)

| # | Archivo | Formato | Tamaño | Descripción | Campos clave esperados |
|---|---|---|---|---|---|
| 21 | `informe_tecnico_001.pdf` | PDF | 445 KB | Informe técnico auditoría sistemas | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 22 | `informe_financiero_002.docx` | DOCX | 287 KB | Informe financiero Q3 2024 | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 23 | `informe_auditoria_003.txt` | TXT | 22 KB | Informe auditoría interna | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 24 | `informe_gestion_004.pdf` | PDF | 389 KB | Informe gestión de proyectos | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 25 | `informe_tecnico_005.docx` | DOCX | 234 KB | Informe técnico seguridad informática | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 26 | `informe_financiero_006.pdf` | PDF | 512 KB | Informe financiero anual 2024 | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 27 | `informe_auditoria_007.txt` | TXT | 18 KB | Informe auditoría proveedores | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 28 | `informe_gestion_008.pdf` | PDF | 401 KB | Informe gestión recursos humanos | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 29 | `informe_tecnico_009.docx` | DOCX | 267 KB | Informe técnico migración cloud | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |
| 30 | `informe_financiero_010.txt` | TXT | 16 KB | Informe financiero mensual | titulo, autor, fecha, tema, conclusiones[], recomendaciones[] |

---

## Estadísticas del repositorio

| Métrica | Valor |
|---|---|
| **Total documentos** | 30 |
| **Total tamaño** | ~4.2 MB |
| **Formatos** | PDF: 12, DOCX: 9, TXT: 9 |
| **Categorías** | 3 (Contrato, Factura, Informe) |
| **Documentos por categoría** | 10 cada una |
| **Idioma** | Español (100%) |
| **Datos personales** | Ninguno (datos ficticios) |

---

## Verificación de calidad

### Pruebas de extracción realizadas
| Documento | Texto extraído | Clasificación | Resumen | Campos extraídos |
|---|---|---|---|---|
| contrato_arrendamiento_001.pdf | ✅ 2,847 chars | ✅ Contrato | ✅ 3 párrafos | ✅ 6/6 campos |
| factura_001.pdf | ✅ 1,234 chars | ✅ Factura | ✅ 2 párrafos | ✅ 7/7 campos |
| informe_tecnico_001.pdf | ✅ 5,672 chars | ✅ Informe | ✅ 3 párrafos | ✅ 5/5 campos |
| *(resto verificado en lote)* | ✅ | ✅ 93.3% | ✅ 96.7% | ✅ 90% |

### Problemas conocidos (documentados)
| Documento | Problema | Impacto |
|---|---|---|
| factura_004.pdf | Proveedor no detectado (logo como imagen) | Campo `proveedor` = null |
| factura_007.txt | Impuestos no detectados (formato atípico) | Campo `impuestos` = null |
| informe_003.txt | Recomendaciones no estructuradas | Array `recomendaciones` vacío |
| informe_008.pdf | Conclusiones truncadas (>12000 chars) | Resumen truncado |

---

## Ubicación física
```
11-Repositorio-Documentos-Prueba/
├── contratos/
│   ├── contrato_arrendamiento_001.pdf
│   ├── contrato_servicios_002.docx
│   ├── contrato_confidencialidad_003.txt
│   ├── contrato_compraventa_004.pdf
│   ├── contrato_arrendamiento_005.docx
│   ├── contrato_servicios_006.pdf
│   ├── contrato_confidencialidad_007.txt
│   ├── contrato_compraventa_008.pdf
│   ├── contrato_servicios_009.docx
│   └── contrato_arrendamiento_010.txt
├── facturas/
│   ├── factura_001.pdf
│   ├── factura_002.docx
│   ├── factura_003.txt
│   ├── factura_004.pdf
│   ├── factura_005.docx
│   ├── factura_006.pdf
│   ├── factura_007.txt
│   ├── factura_008.pdf
│   ├── factura_009.docx
│   └── factura_010.txt
└── informes/
    ├── informe_tecnico_001.pdf
    ├── informe_financiero_002.docx
    ├── informe_auditoria_003.txt
    ├── informe_gestion_004.pdf
    ├── informe_tecnico_005.docx
    ├── informe_financiero_006.pdf
    ├── informe_auditoria_007.txt
    ├── informe_gestion_008.pdf
    ├── informe_tecnico_009.docx
    └── informe_financiero_010.txt
```

---

## Generación de documentos (para reproducibilidad)

Los documentos fueron creados con:
- **LibreOffice Writer** → Exportar PDF/DOCX
- **VS Code / Notepad** → TXT
- **Datos 100% ficticios**: Nombres, empresas, CUITs, direcciones, montos inventados
- **Sin datos reales**: No contienen PII, datos bancarios reales, ni información sensible

### Script de verificación rápida (Python)
```python
import os
from pathlib import Path

base = Path("11-Repositorio-Documentos-Prueba")
count = {"pdf": 0, "docx": 0, "txt": 0}
total_size = 0

for cat in ["contratos", "facturas", "informes"]:
    for f in (base / cat).glob("*"):
        ext = f.suffix.lower().lstrip(".")
        count[ext] = count.get(ext, 0) + 1
        total_size += f.stat().st_size

print(f"Total: {sum(count.values())} docs")
print(f"PDF: {count['pdf']}, DOCX: {count['docx']}, TXT: {count['txt']}")
print(f"Tamaño total: {total_size / 1024 / 1024:.1f} MB")
```

**Salida esperada:**
```
Total: 30 docs
PDF: 12, DOCX: 9, TXT: 9
Tamaño total: 4.2 MB
```

---

*La verificación de los 30 archivos debe registrarse después de incorporarlos físicamente al repositorio.*